# Central configuration for the PersonaPulseAI support agent

import os
from dotenv import load_dotenv

load_dotenv()

# Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL   = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
EMBEDDING_MODEL = "gemini-embedding-2"

# RAG / Vector DB
DATA_DIR        = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
CHROMA_DB_DIR   = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chroma_db")
COLLECTION_NAME = "nexacloud_support_kb"

CHUNK_SIZE    = 400   # characters per chunk
CHUNK_OVERLAP = 40    # overlap between adjacent chunks
TOP_K         = 3     # number of chunks to retrieve

# Escalation thresholds
# Tuned by running test queries — feel free to adjust
CONFIDENCE_THRESHOLD         = 0.40   # below this cosine score → escalate
MAX_FRUSTRATION_TURNS        = 3      # n consecutive frustrated turns → escalate

# Keywords that always trigger escalation regardless of retrieval score
SENSITIVE_KEYWORDS = [
    "lawsuit", "legal action", "fraud", "chargeback", "stolen",
    "hacked", "lawyer", "court", "sue", "attorney", "police",
    "report you", "data breach", "regulatory complaint"
]

# Billing issues that need a human to review
BILLING_ESCALATION_KEYWORDS = [
    "duplicate charge", "overcharged", "wrong charge",
    "billing error", "unauthorized charge", "demand refund",
    "immediate refund", "charge back", "dispute charge"
]

# Persona display colors (used in the UI)
PERSONA_COLORS = {
    "Technical Expert":    "#3b82f6",   # blue
    "Frustrated User":     "#ef4444",   # red
    "Business Executive":  "#10b981",   # green
}

PERSONA_ICONS = {
    "Technical Expert":   "🔧",
    "Frustrated User":    "😤",
    "Business Executive": "💼",
}
