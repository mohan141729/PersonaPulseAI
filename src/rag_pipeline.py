# RAG Pipeline module using ChromaDB and Gemini Embeddings

import os
import time
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from google import genai
import chromadb

from src.config import (
    GEMINI_API_KEY, EMBEDDING_MODEL,
    DATA_DIR, CHROMA_DB_DIR, COLLECTION_NAME,
    CHUNK_SIZE, CHUNK_OVERLAP, TOP_K
)


class RAGPipeline:
    def __init__(self):
        self.genai_client  = genai.Client(api_key=GEMINI_API_KEY)
        self.chroma_client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
        self.collection    = self.chroma_client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}   # cosine similarity
        )
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            separators=["\n\n", "\n", ". ", " ", ""]
        )

    # document loading

    def _load_text_file(self, path: str) -> str:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    def _load_pdf(self, path: str) -> str:
        reader = PdfReader(path)
        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        return text

    def _load_all_documents(self) -> list[dict]:
        """
        Walks the data/ directory and loads all supported files.
        Returns a list of {"name": str, "content": str} dicts.
        """
        docs = []
        supported = (".md", ".txt", ".pdf")

        if not os.path.exists(DATA_DIR):
            print(f"[RAG] Warning: data directory not found at {DATA_DIR}")
            return docs

        for filename in sorted(os.listdir(DATA_DIR)):
            if not filename.endswith(supported):
                continue

            filepath = os.path.join(DATA_DIR, filename)
            try:
                if filename.endswith(".pdf"):
                    content = self._load_pdf(filepath)
                else:
                    content = self._load_text_file(filepath)

                if content.strip():
                    docs.append({"name": filename, "content": content})
                    print(f"[RAG] Loaded: {filename} ({len(content)} chars)")
            except Exception as e:
                print(f"[RAG] Error loading {filename}: {e}")

        return docs

    # embedding

    def _get_embedding(self, text: str, retries: int = 5) -> list[float]:
        # Calls Gemini embedding API with basic retry logic
        for attempt in range(retries):
            try:
                response = self.genai_client.models.embed_content(
                    model=EMBEDDING_MODEL,
                    contents=text
                )
                return response.embeddings[0].values
            except Exception as e:
                if attempt < retries - 1:
                    time.sleep(3)
                else:
                    raise e

    # indexing

    def index_documents(self):
        """
        Loads all documents, chunks them, embeds each chunk, and stores in ChromaDB.
        Run this once — subsequent app starts just load from disk.
        """
        docs = self._load_all_documents()
        if not docs:
            print("[RAG] No documents found to index.")
            return

        total_chunks = 0
        for doc in docs:
            chunks = self.splitter.split_text(doc["content"])
            doc_name = os.path.splitext(doc["name"])[0]  # strip extension for cleaner metadata

            print(f"[RAG] Indexing {doc['name']} -> {len(chunks)} chunks...")

            for i, chunk in enumerate(chunks):
                chunk_id = f"{doc_name}__chunk_{i}"

                # skip if already indexed (so we can re-run safely)
                existing = self.collection.get(ids=[chunk_id])
                if existing["ids"]:
                    continue

                embedding = self._get_embedding(chunk)
                self.collection.add(
                    ids=[chunk_id],
                    embeddings=[embedding],
                    documents=[chunk],
                    metadatas=[{
                        "source":      doc["name"],
                        "doc_name":    doc_name,
                        "chunk_index": i,
                        "section":     self._guess_section(chunk)
                    }]
                )
                total_chunks += 1

                # small sleep to avoid hammering the embedding API
                time.sleep(0.1)

        print(f"[RAG] Indexing complete. Total chunks stored: {total_chunks}")

    def _guess_section(self, chunk: str) -> str:
        """Try to extract a section heading from the chunk text for metadata."""
        lines = chunk.strip().split("\n")
        for line in lines[:3]:
            line = line.strip()
            if line.startswith("#"):
                return line.lstrip("#").strip()
        return "General"

    def is_indexed(self) -> bool:
        """Check if the collection already has documents."""
        return self.collection.count() > 0

    def load_or_build_index(self):
        """Call this on app startup — builds index only if not already done."""
        count = self.collection.count()
        if count > 0:
            print(f"[RAG] Index already exists with {count} chunks. Skipping re-indexing.")
        else:
            print("[RAG] No index found. Building from scratch...")
            self.index_documents()

    # retrieval

    def retrieve(self, query: str, top_k: int = TOP_K) -> list[dict]:
        """
        Embeds the query and retrieves the top-k most similar chunks.

        Returns a list of dicts:
        [
            {
                "text":       str,    # chunk content
                "source":     str,    # filename
                "doc_name":   str,    # filename without extension
                "section":    str,    # section heading
                "chunk_index": int,
                "confidence": float  # 1 - cosine_distance (0-1)
            },
            ...
        ]
        """
        if self.collection.count() == 0:
            print("[RAG] Warning: collection is empty. Did you run indexing?")
            return []

        query_embedding = self._get_embedding(query)

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(top_k, self.collection.count()),
            include=["documents", "metadatas", "distances"]
        )

        retrieved = []
        if not results or not results.get("documents"):
            return retrieved

        docs      = results["documents"][0]
        metas     = results["metadatas"][0]
        distances = results["distances"][0]

        for doc, meta, dist in zip(docs, metas, distances):
            # cosine distance in ChromaDB is 0 (same) to 1 (opposite)
            confidence = round(1.0 - dist, 4)
            retrieved.append({
                "text":        doc,
                "source":      meta.get("source", "unknown"),
                "doc_name":    meta.get("doc_name", "unknown"),
                "section":     meta.get("section", "General"),
                "chunk_index": meta.get("chunk_index", 0),
                "confidence":  confidence
            })

        return retrieved

    def get_best_confidence(self, chunks: list[dict]) -> float:
        """Returns the highest confidence score from retrieved chunks."""
        if not chunks:
            return 0.0
        return max(c["confidence"] for c in chunks)
