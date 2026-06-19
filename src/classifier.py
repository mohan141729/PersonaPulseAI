# Persona classifier module

import json
import re
from google import genai
from google.genai import types
from src.config import GEMINI_API_KEY, GEMINI_MODEL


def classify_persona(user_message: str) -> dict:
    # Classify the user message to get the persona and sentiment
    client = genai.Client(api_key=GEMINI_API_KEY)

    system_prompt = (
        "You are a customer persona classification engine for a SaaS product support system.\n\n"
        "Analyze the tone, vocabulary, urgency level, and intent of the support message below "
        "and classify it into EXACTLY ONE of these three personas:\n\n"
        "1. 'Technical Expert'  — Uses technical jargon (APIs, error codes, logs, tokens, configs). "
        "Wants detailed explanations and root cause analysis.\n"
        "2. 'Frustrated User'   — Uses emotional or urgent language (exclamation marks, "
        "'nothing works', 'I've tried everything', desperation). Needs empathy.\n"
        "3. 'Business Executive' — Focused on business outcomes, timelines, ROI, operational impact. "
        "Prefers concise, high-level answers.\n\n"
        "Also, analyze the overall sentiment of the user's message (Positive, Neutral, or Negative).\n\n"
        "Return ONLY a valid JSON object. Do not include markdown or explanation outside the JSON."
    )

    response_schema = {
        "type": "OBJECT",
        "properties": {
            "persona": {
                "type": "STRING",
                "enum": ["Technical Expert", "Frustrated User", "Business Executive"]
            },
            "confidence": {"type": "NUMBER"},
            "reasoning": {"type": "STRING"},
            "sentiment": {
                "type": "STRING",
                "enum": ["Positive", "Neutral", "Negative"]
            }
        },
        "required": ["persona", "confidence", "reasoning", "sentiment"]
    }

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type="application/json",
                response_schema=response_schema,
                temperature=0.1,  # low temp → consistent classification
            )
        )
        result = json.loads(response.text)
        # clamp confidence to [0, 1] just in case
        result["confidence"] = max(0.0, min(1.0, float(result.get("confidence", 0.5))))
        return result

    except Exception as e:
        print(f"[classifier] Gemini API error — falling back to keyword matching. Error: {e}")
        return _keyword_fallback(user_message)


def _keyword_fallback(message: str) -> dict:
    # Basic fallback using keyword counts if API fails
    msg = message.lower()

    tech_words = [
        "api", "error", "log", "token", "oauth", "endpoint", "config",
        "ssl", "http", "status code", "401", "403", "500", "debug",
        "authentication", "integration", "payload", "header", "sdk",
        "rate limit", "webhook", "jwt", "hmac", "bash", "curl"
    ]
    exec_words = [
        "business", "impact", "operations", "timeline", "resolution time",
        "sla", "roi", "our team", "productivity", "downtime", "escalate",
        "management", "contract", "enterprise", "when will"
    ]
    frustrated_words = [
        "!", "frustrated", "nothing works", "tried everything", "still broken",
        "hours", "days", "ridiculous", "unacceptable", "worst", "fix this",
        "urgent", "asap", "immediately", "can't believe", "useless"
    ]

    scores = {
        "Technical Expert":    sum(1 for w in tech_words if w in msg),
        "Business Executive":  sum(1 for w in exec_words if w in msg),
        "Frustrated User":     sum(1 for w in frustrated_words if w in msg),
    }

    # count exclamation marks as frustration signal
    scores["Frustrated User"] += msg.count("!")

    best = max(scores, key=scores.get)
    if scores[best] == 0:
        # can't tell → default to Frustrated User (most common in support)
        best = "Frustrated User"

    confidence = min(scores[best] * 0.15, 0.70)

    return {
        "persona": best,
        "confidence": confidence,
        "reasoning": "Classified using keyword heuristics (API unavailable)",
        "sentiment": "Negative" if best == "Frustrated User" else "Neutral"
    }
