# Main Streamlit web application
# Run with: streamlit run app.py

# pyrefly: ignore [missing-import]
import streamlit as st
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from src.classifier import classify_persona
from src.rag_pipeline import RAGPipeline
from src.generator import generate_response
from src.escalator import check_escalation, generate_handoff_summary, format_handoff_for_display
from src.config import PERSONA_COLORS, PERSONA_ICONS

# Page config (must be first Streamlit call)
st.set_page_config(
    page_title="PersonaPulseAI — Support Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
  /* Import font */
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

  html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
  }

  /* Main background */
  .stApp {
    background: linear-gradient(135deg, #0d0d1a 0%, #0f1421 50%, #0d0d1a 100%);
  }

  /* Hide default Streamlit header */
  #MainMenu, footer, header { visibility: hidden; }

  /* Hero header */
  .hero-header {
    background: linear-gradient(135deg, #1a0533 0%, #0f1940 50%, #0a1628 100%);
    border: 1px solid rgba(139, 92, 246, 0.25);
    border-radius: 16px;
    padding: 28px 36px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
  }
  .hero-header::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle at 30% 40%, rgba(139,92,246,0.08) 0%, transparent 60%);
    pointer-events: none;
  }
  .hero-title {
    font-size: 2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #a78bfa, #6366f1, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
    line-height: 1.2;
  }
  .hero-subtitle {
    color: #94a3b8;
    font-size: 0.9rem;
    margin-top: 6px;
    font-weight: 400;
  }

  /* Chat bubbles */
  .msg-user {
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    color: #ffffff;
    border-radius: 18px 18px 4px 18px;
    padding: 14px 18px;
    margin: 8px 0 8px 15%;
    line-height: 1.6;
    font-size: 0.92rem;
    box-shadow: 0 4px 20px rgba(99,102,241,0.3);
  }
  .msg-bot {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.09);
    color: #e2e8f0;
    border-radius: 4px 18px 18px 18px;
    padding: 16px 20px;
    margin: 8px 15% 8px 0;
    line-height: 1.7;
    font-size: 0.92rem;
    backdrop-filter: blur(8px);
  }
  .msg-label-user {
    text-align: right;
    color: #94a3b8;
    font-size: 0.72rem;
    margin-bottom: 4px;
    margin-right: 4px;
    font-weight: 500;
    letter-spacing: 0.05em;
    text-transform: uppercase;
  }
  .msg-label-bot {
    color: #94a3b8;
    font-size: 0.72rem;
    margin-bottom: 4px;
    margin-left: 4px;
    font-weight: 500;
    letter-spacing: 0.05em;
    text-transform: uppercase;
  }

  /* Persona badge */
  .persona-badge {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    margin-bottom: 10px;
    border: 1px solid;
  }
  .badge-tech {
    background: rgba(59, 130, 246, 0.15);
    color: #93c5fd;
    border-color: rgba(59, 130, 246, 0.4);
  }
  .badge-frustrated {
    background: rgba(239, 68, 68, 0.15);
    color: #fca5a5;
    border-color: rgba(239, 68, 68, 0.4);
  }
  .badge-exec {
    background: rgba(16, 185, 129, 0.15);
    color: #6ee7b7;
    border-color: rgba(16, 185, 129, 0.4);
  }

  /* Source card */
  .source-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-left: 3px solid #6366f1;
    border-radius: 8px;
    padding: 10px 14px;
    margin: 6px 0;
    font-size: 0.8rem;
    color: #94a3b8;
  }
  .source-name {
    color: #a78bfa;
    font-weight: 600;
    font-size: 0.82rem;
  }
  .source-conf {
    color: #10b981;
    font-size: 0.75rem;
    font-weight: 600;
  }
  .source-text {
    color: #64748b;
    font-size: 0.78rem;
    margin-top: 4px;
    line-height: 1.4;
  }

  /* Escalation alert */
  .escalation-alert {
    background: rgba(220, 38, 38, 0.1);
    border: 1px solid rgba(220, 38, 38, 0.4);
    border-radius: 10px;
    padding: 14px 18px;
    margin: 10px 0;
    color: #fca5a5;
    font-size: 0.88rem;
  }
  .escalation-title {
    font-weight: 700;
    font-size: 0.92rem;
    color: #f87171;
    margin-bottom: 4px;
  }

  /* Sidebar styling */
  [data-testid="stSidebar"] {
    background: rgba(10, 10, 25, 0.95) !important;
    border-right: 1px solid rgba(255,255,255,0.07) !important;
  }
  .sidebar-section {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 10px;
    padding: 14px 16px;
    margin: 10px 0;
  }
  .sidebar-title {
    color: #a78bfa;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 8px;
  }
  .stat-row {
    display: flex;
    justify-content: space-between;
    color: #94a3b8;
    font-size: 0.8rem;
    padding: 3px 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
  }
  .stat-val {
    color: #e2e8f0;
    font-weight: 600;
  }

  /* Confidence bar */
  .conf-bar-bg {
    background: rgba(255,255,255,0.08);
    border-radius: 99px;
    height: 6px;
    margin: 6px 0;
    overflow: hidden;
  }
  .conf-bar-fill {
    height: 100%;
    border-radius: 99px;
    background: linear-gradient(90deg, #6366f1, #10b981);
    transition: width 0.4s ease;
  }

  /* Thinking spinner */
  .thinking-dots {
    color: #6366f1;
    font-size: 1.5rem;
    letter-spacing: 4px;
    animation: pulse 1.2s infinite;
  }
  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.3; }
  }

  /* Input box */
  .stTextInput > div > div > input,
  .stChatInputContainer textarea {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
    font-family: 'Inter', sans-serif !important;
  }

  /* Expander */
  .streamlit-expanderHeader {
    background: rgba(255,255,255,0.03) !important;
    border-radius: 8px !important;
    color: #94a3b8 !important;
    font-size: 0.82rem !important;
  }

  /* JSON block */
  .stCodeBlock {
    border-radius: 10px !important;
    font-size: 0.78rem !important;
  }

  /* scrollbar */
  ::-webkit-scrollbar { width: 6px; }
  ::-webkit-scrollbar-track { background: transparent; }
  ::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.3); border-radius: 99px; }
</style>
""", unsafe_allow_html=True)


# Session state init
def init_session():
    defaults = {
        "messages":           [],        # chat history: {role, content, meta}
        "conversation_history": [],      # for LLM context: {role, content}
        "frustration_count":  0,
        "escalated":          False,
        "turn_count":         0,
        "last_persona":       None,
        "last_confidence":    0.0,
        "index_ready":        False,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_session()


# Load RAG pipeline (cached across reruns)
@st.cache_resource(show_spinner=False)
def load_pipeline():
    pipeline = RAGPipeline()
    pipeline.load_or_build_index()
    return pipeline


# Helper: persona badge HTML
def persona_badge_html(persona: str) -> str:
    icon = PERSONA_ICONS.get(persona, "👤")
    css_class = {
        "Technical Expert":   "badge-tech",
        "Frustrated User":    "badge-frustrated",
        "Business Executive": "badge-exec",
    }.get(persona, "badge-tech")
    return f'<span class="persona-badge {css_class}">{icon} {persona}</span>'


# Helper: confidence color
def conf_color(score: float) -> str:
    if score >= 0.65: return "#10b981"
    if score >= 0.45: return "#f59e0b"
    return "#ef4444"


# Render a single chat message
def render_message(msg: dict):
    role = msg["role"]
    content = msg["content"]
    meta = msg.get("meta", {})

    if role == "user":
        st.markdown(f'<div class="msg-label-user">You</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="msg-user">{content}</div>', unsafe_allow_html=True)

    else:
        persona    = meta.get("persona", "")
        chunks     = meta.get("chunks", [])
        escalated  = meta.get("escalated", False)
        esc_reason = meta.get("escalation_reason", "")
        handoff    = meta.get("handoff", None)
        confidence = meta.get("best_confidence", 0.0)
        sentiment  = meta.get("sentiment", "Neutral")

        st.markdown(f'<div class="msg-label-bot">PersonaPulseAI</div>', unsafe_allow_html=True)

        # Persona badge + confidence
        badge_html = persona_badge_html(persona) if persona else ""
        conf_pct   = int(confidence * 100)
        color      = conf_color(confidence)
        conf_html  = (
            f'<span style="font-size:0.75rem; color:{color}; font-weight:600; margin-left:8px;">'
            f'⬡ {conf_pct}% match</span>'
        ) if confidence > 0 else ""

        # Sentiment badge
        sent_icon = "🟢" if sentiment == "Positive" else "🔴" if sentiment == "Negative" else "⚪"
        sent_html = f'<span style="font-size:0.75rem; color:#94a3b8; font-weight:600; margin-left:8px;">{sent_icon} {sentiment}</span>' if persona else ""

        st.markdown(f'{badge_html}{conf_html}{sent_html}', unsafe_allow_html=True)

        # Bot response bubble
        # Replace newlines with <br> for HTML rendering
        html_content = content.replace("\n", "<br>")
        st.markdown(f'<div class="msg-bot">{html_content}</div>', unsafe_allow_html=True)

        # Escalation alert
        if escalated:
            st.markdown(f"""
            <div class="escalation-alert">
                <div class="escalation-title">🚨 Escalated to Human Agent</div>
                {esc_reason}
            </div>
            """, unsafe_allow_html=True)

            if handoff:
                with st.expander("📋 View Handoff Summary (JSON)", expanded=False):
                    st.code(format_handoff_for_display(handoff), language="json")

        # Retrieved sources
        if chunks:
            with st.expander(f"📚 Retrieved Sources ({len(chunks)})", expanded=False):
                for i, chunk in enumerate(chunks, 1):
                    conf_pct_chunk = int(chunk["confidence"] * 100)
                    preview = chunk["text"][:180].replace("\n", " ").strip()
                    if len(chunk["text"]) > 180:
                        preview += "..."
                    st.markdown(f"""
                    <div class="source-card">
                        <div>
                            <span class="source-name">📄 {chunk['doc_name']}</span>
                            &nbsp;·&nbsp;
                            <span style="color:#64748b; font-size:0.75rem;">§ {chunk['section']}</span>
                            &nbsp;&nbsp;
                            <span class="source-conf">↑ {conf_pct_chunk}%</span>
                        </div>
                        <div class="source-text">{preview}</div>
                    </div>
                    """, unsafe_allow_html=True)


# Sidebar
def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center; padding: 12px 0 20px 0;">
            <div style="font-size:2.2rem;">🤖</div>
            <div style="font-size:1.1rem; font-weight:700; color:#a78bfa; margin-top:4px;">PersonaPulseAI</div>
            <div style="font-size:0.72rem; color:#475569; margin-top:2px;">Persona-Adaptive Support Agent</div>
        </div>
        """, unsafe_allow_html=True)

        # Session stats
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-title">Session Stats</div>', unsafe_allow_html=True)

        last_persona = st.session_state.last_persona or "—"
        icon = PERSONA_ICONS.get(last_persona, "") if last_persona != "—" else ""
        color = PERSONA_COLORS.get(last_persona, "#94a3b8") if last_persona != "—" else "#94a3b8"

        stats = [
            ("Messages",       str(st.session_state.turn_count)),
            ("Current Persona", f"{icon} {last_persona}"),
            ("Escalated",      "Yes 🚨" if st.session_state.escalated else "No ✅"),
        ]
        for label, val in stats:
            st.markdown(f"""
            <div class="stat-row">
                <span>{label}</span>
                <span class="stat-val" style="color:{color if label=='Current Persona' else '#e2e8f0'}">{val}</span>
            </div>
            """, unsafe_allow_html=True)

        # Confidence bar
        if st.session_state.last_confidence > 0:
            conf_pct = int(st.session_state.last_confidence * 100)
            c_color = conf_color(st.session_state.last_confidence)
            st.markdown(f"""
            <div style="margin-top:8px;">
                <div style="display:flex; justify-content:space-between; font-size:0.75rem; color:#64748b;">
                    <span>Retrieval Confidence</span>
                    <span style="color:{c_color}; font-weight:600;">{conf_pct}%</span>
                </div>
                <div class="conf-bar-bg">
                    <div class="conf-bar-fill" style="width:{conf_pct}%; background: linear-gradient(90deg, {c_color}, {c_color}aa);"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Persona legend
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-title">Persona Types</div>', unsafe_allow_html=True)
        personas_info = {
            "Technical Expert":   ("🔧", "#3b82f6", "API errors, configs, logs"),
            "Frustrated User":    ("😤", "#ef4444", "Urgency, emotional language"),
            "Business Executive": ("💼", "#10b981", "Impact, timelines, outcomes"),
        }
        for name, (icon, color, desc) in personas_info.items():
            st.markdown(f"""
            <div style="padding: 5px 0; border-bottom: 1px solid rgba(255,255,255,0.04);">
                <span style="color:{color}; font-weight:600; font-size:0.8rem;">{icon} {name}</span>
                <div style="color:#475569; font-size:0.72rem; margin-top:1px;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Controls
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-title">Controls</div>', unsafe_allow_html=True)
        if st.button("🗑️ Clear Conversation", use_container_width=True):
            st.session_state.messages = []
            st.session_state.conversation_history = []
            st.session_state.frustration_count = 0
            st.session_state.escalated = False
            st.session_state.turn_count = 0
            st.session_state.last_persona = None
            st.session_state.last_confidence = 0.0
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        # About
        with st.expander("ℹ️ About this project"):
            st.markdown("""
            **PersonaPulseAI** is a final year B.Tech project demonstrating:
            - 🎯 LLM-based persona detection
            - 📚 RAG with ChromaDB
            - 🔄 Adaptive response generation
            - 🚨 Automatic escalation logic

            **Stack:** Python · Gemini · ChromaDB · LangChain · Streamlit

            *Knowledge base: NexaCloud SaaS (fictional)*
            """)


# Main app
def main():
    render_sidebar()

    # Hero header
    st.markdown("""
    <div class="hero-header">
        <div class="hero-title">🤖 PersonaPulseAI</div>
        <div class="hero-subtitle">
            Intelligent support agent that adapts to your communication style.
            Powered by Gemini · RAG · ChromaDB
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Load the pipeline (auto-indexes on first run)
    with st.spinner("⚙️ Loading knowledge base... (first run may take 1–3 minutes)"):
        try:
            pipeline = load_pipeline()
            st.session_state.index_ready = True
        except Exception as e:
            st.error(f"❌ Failed to load pipeline: {e}")
            st.info("Make sure your GEMINI_API_KEY is set in the .env file.")
            return

    # Show example prompts if no messages yet
    if not st.session_state.messages:
        st.markdown("""
        <div style="text-align:center; padding: 30px 0 20px 0; color: #475569; font-size: 0.88rem;">
            💬 Start a conversation below. Try one of these examples:
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        example_queries = [
            ("🔧 Technical", "Our API is returning 401 Unauthorized even though the key was just generated. Can you check the OAuth token validation flow?"),
            ("😤 Frustrated", "I've been trying to reset my password for 2 hours and nothing is working!! The emails never arrive!"),
            ("💼 Executive",  "How does the current service downtime impact our SLA commitments and what's the expected resolution timeline?"),
        ]
        for col, (label, query) in zip([col1, col2, col3], example_queries):
            with col:
                if st.button(label, key=f"ex_{label}", use_container_width=True, help=query):
                    st.session_state._prefill = query
                    st.rerun()

    # Render chat history
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.messages:
            render_message(msg)

    # Chat input
    # Handle pre-filled query from example buttons
    prefill = st.session_state.pop("_prefill", None)

    user_input = st.chat_input(
        "Describe your issue or question...",
        disabled=st.session_state.escalated
    )

    # Use prefilled query if available
    query = prefill or user_input

    if st.session_state.escalated and not query:
        st.markdown("""
        <div style="text-align:center; color:#ef4444; font-size:0.85rem; padding:8px;">
            🚨 This conversation has been escalated. Clear the chat to start a new session.
        </div>
        """, unsafe_allow_html=True)

    if query and not st.session_state.escalated:
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": query, "meta": {}})
        st.session_state.conversation_history.append({"role": "user", "content": query})
        st.session_state.turn_count += 1

        # Process the query
        with st.spinner("🧠 Thinking..."):
            try:
                # Step 1: Detect persona
                persona_result = classify_persona(query)
                persona     = persona_result["persona"]
                persona_conf = persona_result["confidence"]
                sentiment   = persona_result.get("sentiment", "Neutral")

                # Track frustration streak
                if persona == "Frustrated User":
                    st.session_state.frustration_count += 1
                else:
                    st.session_state.frustration_count = 0

                st.session_state.last_persona = persona

                # Step 2: Retrieve relevant chunks
                chunks = pipeline.retrieve(query)
                best_confidence = pipeline.get_best_confidence(chunks)
                st.session_state.last_confidence = best_confidence

                # Step 3: Check escalation
                esc_result = check_escalation(
                    user_message=query,
                    persona=persona,
                    chunks=chunks,
                    frustration_turn_count=st.session_state.frustration_count
                )

                if esc_result["should_escalate"]:
                    # Generate escalation response + handoff
                    st.session_state.escalated = True
                    esc_reason = esc_result["reason"]

                    handoff = generate_handoff_summary(
                        user_message=query,
                        persona=persona,
                        chunks=chunks,
                        escalation_reason=esc_reason,
                        conversation_history=st.session_state.conversation_history
                    )

                    # Persona-aware escalation message
                    esc_messages = {
                        "Technical Expert":   "I wasn't able to find sufficient technical documentation for this specific issue. I'm connecting you with a senior engineer who can review logs and provide detailed diagnostics.",
                        "Frustrated User":    "I'm really sorry — I can hear how frustrating this has been, and I want to make sure you get proper help. I'm escalating this to a human support specialist right now who will personally assist you.",
                        "Business Executive": "I need to escalate this to our specialist team to provide you with an accurate resolution timeline and business impact assessment.",
                    }
                    bot_response = esc_messages.get(persona, esc_messages["Frustrated User"])

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": bot_response,
                        "meta": {
                            "persona":           persona,
                            "chunks":            chunks,
                            "escalated":         True,
                            "escalation_reason": esc_reason,
                            "handoff":           handoff,
                            "best_confidence":   best_confidence,
                            "sentiment":         sentiment,
                        }
                    })

                else:
                    # Step 4: Generate persona-adapted response
                    response = generate_response(
                        user_query=query,
                        persona=persona,
                        chunks=chunks,
                        conversation_history=st.session_state.conversation_history
                    )

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response,
                        "meta": {
                            "persona":           persona,
                            "chunks":            chunks,
                            "escalated":         False,
                            "escalation_reason": "",
                            "handoff":           None,
                            "best_confidence":   best_confidence,
                            "sentiment":         sentiment,
                        }
                    })

                    st.session_state.conversation_history.append({
                        "role": "assistant",
                        "content": response
                    })

            except Exception as e:
                st.error(f"Something went wrong: {e}")
                st.info("Check your GEMINI_API_KEY and internet connection.")
                st.stop()

        st.rerun()


if __name__ == "__main__":
    main()
