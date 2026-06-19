"""
ingest.py
---------
Standalone script to build the ChromaDB vector index from the data/ directory.
Run this BEFORE starting the app if you want to pre-build the index,
or if you've added new documents and want to re-index.

Usage:
    python ingest.py           # full index build
    python ingest.py --reset   # wipe existing index and rebuild from scratch

Note: This takes 1-3 minutes depending on how many documents/chunks there are,
because we need to call the Gemini embedding API for each chunk.
"""

import sys
import os
import shutil
import argparse

# make sure src/ is importable when running from project root
sys.path.insert(0, os.path.dirname(__file__))

from src.rag_pipeline import RAGPipeline
from src.config import CHROMA_DB_DIR, DATA_DIR


def main():
    parser = argparse.ArgumentParser(description="Ingest documents into ChromaDB")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Delete existing index and rebuild from scratch"
    )
    args = parser.parse_args()

    print("=" * 55)
    print("  PersonaPulseAI — Knowledge Base Ingestion")
    print("=" * 55)

    # Check data directory exists
    if not os.path.exists(DATA_DIR):
        print(f"[!] Data directory not found: {DATA_DIR}")
        print("    Create the data/ folder and add your documents first.")
        sys.exit(1)

    # Count available documents
    supported = (".md", ".txt", ".pdf")
    doc_files = [f for f in os.listdir(DATA_DIR) if f.endswith(supported)]
    print(f"\n[+] Found {len(doc_files)} document(s) in {DATA_DIR}:")
    for f in doc_files:
        size_kb = os.path.getsize(os.path.join(DATA_DIR, f)) // 1024
        print(f"    - {f} ({size_kb} KB)")

    # Handle reset
    if args.reset and os.path.exists(CHROMA_DB_DIR):
        print(f"\n[!] --reset flag set. Deleting existing index at {CHROMA_DB_DIR}...")
        shutil.rmtree(CHROMA_DB_DIR)
        print("[+] Existing index deleted.")

    print(f"\n[+] Initializing RAG pipeline...")
    pipeline = RAGPipeline()

    if pipeline.is_indexed() and not args.reset:
        count = pipeline.collection.count()
        print(f"[+] Index already exists ({count} chunks). Use --reset to rebuild.")
        print("\nDone! The app is ready to run: streamlit run app.py")
        return

    print("[+] Starting document ingestion. This may take 1-3 minutes...\n")
    pipeline.index_documents()

    final_count = pipeline.collection.count()
    print(f"\n{'='*55}")
    print(f"  Ingestion complete!")
    print(f"  Total chunks indexed: {final_count}")
    print(f"  Vector DB saved at:   {CHROMA_DB_DIR}")
    print(f"{'='*55}")
    print("\nYou can now run the app: streamlit run app.py")


if __name__ == "__main__":
    main()
