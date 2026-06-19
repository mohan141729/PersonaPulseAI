# Escalation engine to route issues to human agents

import json
from datetime import datetime
from src.config import (
    CONFIDENCE_THRESHOLD,
    MAX_FRUSTRATION_TURNS,
    SENSITIVE_KEYWORDS,
    BILLING_ESCALATION_KEYWORDS
)


def check_escalation(
    user_message: str,
    persona: str,
    chunks: list[dict],
    frustration_turn_count: int = 0
) -> dict:
    # Check triggers for escalation
    msg_lower = user_message.lower()

    # Trigger 1: No documents found
    if not chunks:
        return {
            "should_escalate": True,
            "reason": "No relevant documents were found in the knowledge base for this query.",
            "trigger": "NO_DOCUMENTS"
        }

    # Trigger 2: Sensitive legal / security keywords
    for kw in SENSITIVE_KEYWORDS:
        if kw in msg_lower:
            return {
                "should_escalate": True,
                "reason": f"Message contains sensitive keyword: '{kw}'. Requires human review.",
                "trigger": "SENSITIVE_KEYWORD"
            }

    # Trigger 3: Billing dispute keywords
    for kw in BILLING_ESCALATION_KEYWORDS:
        if kw in msg_lower:
            return {
                "should_escalate": True,
                "reason": f"Billing dispute detected ('{kw}'). Needs a billing specialist.",
                "trigger": "BILLING_DISPUTE"
            }

    # Trigger 4: Low retrieval confidence
    best_score = max(c["confidence"] for c in chunks)
    if best_score < CONFIDENCE_THRESHOLD:
        return {
            "should_escalate": True,
            "reason": (
                f"Retrieval confidence too low ({best_score:.2f} < {CONFIDENCE_THRESHOLD}). "
                "The knowledge base may not have relevant information for this query."
            ),
            "trigger": "LOW_CONFIDENCE"
        }

    # Trigger 5: Repeated frustration across turns
    if persona == "Frustrated User" and frustration_turn_count >= MAX_FRUSTRATION_TURNS:
        return {
            "should_escalate": True,
            "reason": (
                f"Customer has been frustrated for {frustration_turn_count} consecutive turns "
                "without resolution. Escalating to human support."
            ),
            "trigger": "REPEATED_FRUSTRATION"
        }

    return {
        "should_escalate": False,
        "reason": "",
        "trigger": ""
    }


def generate_handoff_summary(
    user_message: str,
    persona: str,
    chunks: list[dict],
    escalation_reason: str,
    conversation_history: list[dict] | None = None
) -> dict:
    # Create JSON for handoff payload

    # Summarize what was already tried based on conversation history
    attempted_steps = []
    if conversation_history:
        for turn in conversation_history:
            if turn["role"] == "assistant":
                # grab first line of each bot response as a summary of what was suggested
                first_line = turn["content"].split("\n")[0].strip()
                if first_line and first_line not in attempted_steps:
                    attempted_steps.append(first_line[:120])   # cap length

    # Get the sources used
    sources_used = list({c["source"] for c in chunks}) if chunks else []

    # Build recommended next step based on escalation trigger
    recommendations = {
        "NO_DOCUMENTS":        "Manually research the issue. Consider adding documentation to the knowledge base.",
        "SENSITIVE_KEYWORD":   "Review for legal or security implications before responding. Loop in legal/security team.",
        "BILLING_DISPUTE":     "Pull up the customer's billing history. Verify charges and initiate refund review if warranted.",
        "LOW_CONFIDENCE":      "Review the customer's issue in detail. May need to create a new KB article afterward.",
        "REPEATED_FRUSTRATION":"Contact the customer directly (phone or priority email). Issue may need hands-on troubleshooting.",
    }

    # infer trigger from reason (rough match)
    trigger = "LOW_CONFIDENCE"
    for key in recommendations:
        if key.replace("_", " ").lower() in escalation_reason.lower():
            trigger = key
            break
    if "billing" in escalation_reason.lower():
        trigger = "BILLING_DISPUTE"
    if "sensitive" in escalation_reason.lower() or "keyword" in escalation_reason.lower():
        trigger = "SENSITIVE_KEYWORD"
    if "frustrated" in escalation_reason.lower():
        trigger = "REPEATED_FRUSTRATION"
    if "no relevant" in escalation_reason.lower():
        trigger = "NO_DOCUMENTS"

    # Figure out best confidence score
    best_confidence = round(max((c["confidence"] for c in chunks), default=0.0), 3)

    handoff = {
        "escalation_summary": {
            "timestamp":          datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
            "persona":            persona,
            "escalation_trigger": trigger,
            "escalation_reason":  escalation_reason,
        },
        "customer_issue": {
            "message":            user_message,
            "retrieval_confidence": best_confidence,
            "documents_searched": sources_used,
        },
        "conversation_context": {
            "total_turns":        len(conversation_history) if conversation_history else 0,
            "attempted_steps":    attempted_steps if attempted_steps else ["No prior steps taken"],
        },
        "recommended_action":   recommendations.get(trigger, "Review issue manually and respond accordingly.")
    }

    return handoff


def format_handoff_for_display(handoff: dict) -> str:
    # Return as JSON string
    return json.dumps(handoff, indent=2)
