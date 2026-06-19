# Generator module for creating responses

from google import genai
from google.genai import types
from src.config import GEMINI_API_KEY, GEMINI_MODEL


# Persona-specific system prompt templates
_PERSONA_PROMPTS = {
    "Technical Expert": (
        "You are a Senior Technical Support Engineer at NexaCloud.\n"
        "The customer is a technical professional who understands APIs, error codes, and system internals.\n\n"
        "Your response must:\n"
        "- Provide precise root cause analysis where applicable\n"
        "- Include relevant configuration details, HTTP status codes, or command examples\n"
        "- Be structured (numbered steps or clear sections)\n"
        "- Reference specific document sections when useful\n"
        "- Use correct technical terminology — do not oversimplify\n"
        "- Be thorough but not padded with unnecessary filler text"
    ),

    "Frustrated User": (
        "You are a warm, empathetic Customer Care Specialist at NexaCloud.\n"
        "The customer is stressed, frustrated, and needs reassurance.\n\n"
        "Your response must:\n"
        "- Begin with a genuine, human acknowledgment of their frustration (1-2 sentences)\n"
        "- Use simple, plain language — no technical jargon\n"
        "- Break resolution steps into short, numbered bullet points\n"
        "- Keep the tone calm, caring, and reassuring throughout\n"
        "- End with a line offering further help if the steps don't work\n"
        "- Avoid corporate buzzwords or robotic phrasing"
    ),

    "Business Executive": (
        "You are a Client Relations Director at NexaCloud speaking to a senior business stakeholder.\n"
        "This executive wants outcomes, not technical details.\n\n"
        "Your response must:\n"
        "- Get to the point immediately in the first sentence\n"
        "- Focus on business impact, resolution timeline, and next steps\n"
        "- Be concise — ideally under 150 words\n"
        "- Avoid any technical jargon or configuration details\n"
        "- Use a professional, confident tone\n"
        "- If a timeline is mentioned in the documents, include it"
    )
}

_GROUNDING_RULES = (
    "\n\nCRITICAL RULES — follow these without exception:\n"
    "1. Base your ENTIRE response ONLY on the provided context documents below.\n"
    "2. Do NOT invent facts, product features, or steps that are not in the documents.\n"
    "3. If the documents do not contain enough information to fully answer the question, "
    "say so clearly and suggest contacting support.\n"
    "4. Do not mention that you are using provided context — just answer naturally."
)


def build_context_block(chunks: list[dict]) -> str:
    # Build text block from retrieved docs
    if not chunks:
        return "No relevant documents found."

    parts = []
    for i, chunk in enumerate(chunks, 1):
        source_label = f"{chunk['doc_name']} (section: {chunk['section']})"
        parts.append(f"[Document {i} — {source_label}]\n{chunk['text']}")

    return "\n\n---\n\n".join(parts)


def generate_response(
    user_query: str,
    persona: str,
    chunks: list[dict],
    conversation_history: list[dict] | None = None
) -> str:
    # Call Gemini to get response
    client = genai.Client(api_key=GEMINI_API_KEY)

    persona_instruction = _PERSONA_PROMPTS.get(persona, _PERSONA_PROMPTS["Frustrated User"])
    context_block = build_context_block(chunks)

    system_prompt = (
        f"{persona_instruction}"
        f"{_GROUNDING_RULES}\n\n"
        f"KNOWLEDGE BASE CONTEXT:\n{context_block}"
    )

    # Build conversation contents for multi-turn support
    contents = []
    if conversation_history:
        for turn in conversation_history[-6:]:   # last 3 turns = 6 messages
            role = "user" if turn["role"] == "user" else "model"
            contents.append(types.Content(
                role=role,
                parts=[types.Part(text=turn["content"])]
            ))

    contents.append(types.Content(
        role="user",
        parts=[types.Part(text=user_query)]
    ))

    import time
    max_retries = 5
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0.3,    
                    max_output_tokens=800
                )
            )
            return response.text.strip()
        except Exception as e:
            if ("503" in str(e) or "429" in str(e)) and attempt < max_retries - 1:
                time.sleep(3)
                continue
            raise e
