"""Premium AI Health Coach — glass chat UI with persistent history."""
import json
import time
from datetime import datetime

import streamlit as st

from healthhub.config import HISTORY_FILE
from healthhub.styles import hero
from healthhub.services.ai_coach import coach_ready, get_ai_response

_SUGGESTIONS = [
    "Build me a high-protein meal plan",
    "How do I start strength training?",
    "Tips to fall asleep faster",
    "Quick ways to lower stress",
]


def _load_history():
    if HISTORY_FILE.exists():
        try:
            return json.loads(HISTORY_FILE.read_text())
        except Exception:
            return {}
    return {}


def _save_history(data):
    try:
        HISTORY_FILE.write_text(json.dumps(data, indent=2))
    except Exception:
        pass


def _send(user_input):
    chat = st.session_state.health_chat_history
    if not st.session_state.current_conversation_id:
        st.session_state.current_conversation_id = f"conv_{int(time.time())}"
    chat.append({"role": "user", "content": user_input})
    with st.spinner("AI Coach is thinking…"):
        reply = get_ai_response(user_input, chat)
    chat.append({"role": "assistant", "content": reply})

    title = next((m["content"][:32] for m in chat if m["role"] == "user"), "Conversation")
    st.session_state.conversation_history[st.session_state.current_conversation_id] = {
        "messages": chat.copy(),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "title": title,
    }
    _save_history(st.session_state.conversation_history)


def render():
    st.session_state.setdefault("health_chat_history", [])
    st.session_state.setdefault("conversation_history", _load_history())
    st.session_state.setdefault("current_conversation_id", None)

    hero("🤖 AI Health & Wellness Coach",
         "Nutrition · Fitness · Sleep · Mental wellness — personalised, evidence-based guidance.",
         pill="🟢 Live AI Connected" if coach_ready() else "🟡 Smart offline mode")

    st.markdown(
        """
        <div class="feature-grid" style="margin-bottom:22px;">
          <div class="fcard"><div class="ico">🥗</div><h3>Nutrition</h3><p>Personalised diet plans</p></div>
          <div class="fcard"><div class="ico">💪</div><h3>Fitness</h3><p>Custom workout routines</p></div>
          <div class="fcard"><div class="ico">😴</div><h3>Sleep</h3><p>Sleep optimisation tips</p></div>
          <div class="fcard"><div class="ico">🧠</div><h3>Mind</h3><p>Stress management</p></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- Sidebar: conversation history ---
    with st.sidebar:
        history = st.session_state.conversation_history
        st.markdown(
            f'<div style="display:flex;align-items:center;justify-content:space-between;'
            f'margin-bottom:4px;"><span style="font-family:Sora;font-weight:700;font-size:1.05rem;">'
            f'💬 Conversations</span><span style="background:var(--glass-bg);border:1px solid '
            f'var(--glass-brd);border-radius:999px;padding:2px 10px;font-size:.72rem;'
            f'color:var(--muted);">{len(history)}</span></div>',
            unsafe_allow_html=True,
        )
        if st.button("✨ New conversation", use_container_width=True, type="primary"):
            st.session_state.health_chat_history = []
            st.session_state.current_conversation_id = None
            st.rerun()

        if history:
            current = st.session_state.current_conversation_id
            for cid, conv in sorted(history.items(), key=lambda x: x[1]["date"], reverse=True):
                msgs = conv.get("messages", [])
                title = conv.get("title") or "Conversation"
                preview = next((m["content"] for m in reversed(msgs)
                                if m["role"] == "assistant"), "")
                preview = (preview[:90] + "…") if len(preview) > 90 else (preview or "New chat")
                count = len(msgs)
                active = " active" if cid == current else ""
                st.markdown(
                    f"""
                    <div class="hist-card{active}">
                      <div class="hist-row">
                        <span class="hist-ico">💬</span>
                        <span class="hist-title">{title}</span>
                      </div>
                      <div class="hist-preview">{preview}</div>
                      <div class="hist-meta">📅 {conv['date']}<span class="dot"></span>
                        💬 {count} message{'s' if count != 1 else ''}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                c1, c2 = st.columns([3, 1])
                if c1.button("Open ↗", key=f"load_{cid}", use_container_width=True):
                    st.session_state.health_chat_history = conv["messages"].copy()
                    st.session_state.current_conversation_id = cid
                    st.rerun()
                if c2.button("🗑️", key=f"del_{cid}", use_container_width=True):
                    del history[cid]
                    _save_history(history)
                    if current == cid:
                        st.session_state.health_chat_history = []
                        st.session_state.current_conversation_id = None
                    st.rerun()

            st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
            if st.button("🧹 Clear all history", use_container_width=True):
                st.session_state.conversation_history = {}
                st.session_state.health_chat_history = []
                st.session_state.current_conversation_id = None
                _save_history({})
                st.rerun()
        else:
            st.markdown(
                '<div class="glass" style="text-align:center;padding:22px 16px;color:var(--muted);">'
                '<div style="font-size:1.8rem;">🗨️</div>'
                '<div style="margin-top:6px;font-size:.85rem;">No conversations yet</div>'
                '<div style="font-size:.78rem;opacity:.8;">Start chatting to save them here</div></div>',
                unsafe_allow_html=True,
            )

    # --- Suggestion chips (only on empty conversation) ---
    if not st.session_state.health_chat_history:
        st.markdown("##### ✨ Try asking")
        cols = st.columns(2)
        for i, s in enumerate(_SUGGESTIONS):
            if cols[i % 2].button(s, key=f"sugg_{i}", use_container_width=True):
                _send(s)
                st.rerun()

    # --- Chat transcript ---
    for msg in st.session_state.health_chat_history:
        role = "msg-user" if msg["role"] == "user" else "msg-ai"
        who = "You" if msg["role"] == "user" else "Coach"
        st.markdown(f'<div class="{role}"><b>{who}</b><br>{msg["content"]}</div>',
                    unsafe_allow_html=True)

    # --- Input ---
    user_input = st.chat_input("Ask your health question…")
    if user_input:
        _send(user_input)
        st.rerun()
