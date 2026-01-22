import time
import streamlit as st
from openai import OpenAI, RateLimitError

# --------------------
# AUTH (simple password)
# --------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔐 Login")
    password = st.text_input("Enter password", type="password")

    if password == st.secrets.get("APP_PASSWORD"):
        st.session_state.authenticated = True
        st.rerun()
    else:
        st.stop()

# --------------------
# APP SETUP
# --------------------
client = OpenAI()
st.title("🎬 MovieBot")

MODEL = "gpt-5-mini"  # fast + cheaper
MAX_MESSAGES = 10     # cost control

# --------------------
# CHAT MEMORY
# --------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "system",
            "content": "You are MovieBot, a funny, friendly AI who loves movies."
        }
    ]

# --------------------
# CHAT INPUT (SAFE)
# --------------------
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message")
    submitted = st.form_submit_button("Send")

# --------------------
# HANDLE MESSAGE
# --------------------
if submitted and user_input:
    st.session_state.chat_history.append(
        {"role": "user", "content": user_input}
    )

    # Trim history (system + last N)
    st.session_state.chat_history = (
        st.session_state.chat_history[:1]
        + st.session_state.chat_history[-MAX_MESSAGES:]
    )

    assistant_placeholder = st.empty()
    typing_placeholder = st.empty()
    typing_placeholder.markdown("_MovieBot is typing…_")

    full_reply = ""

    try:
        stream = client.chat.completions.create(
            model=MODEL,
            messages=st.session_state.chat_history,
            stream=True
        )

        for chunk in stream:
            if chunk.choices[0].delta.get("content"):
                token = chunk.choices[0].delta.content
                full_reply += token
                assistant_placeholder.markdown(
                    f"<div style='background:#262730;padding:12px;border-radius:10px;'>"
                    f"<b>MovieBot:</b> {full_reply}"
                    f"</div>",
                    unsafe_allow_html=True
                )
                time.sleep(0.02)

    except RateLimitError:
        full_reply = "⏳ I'm getting rate-limited. Please wait a moment and try again."

    typing_placeholder.empty()

    st.session_state.chat_history.append(
        {"role": "assistant", "content": full_reply}
    )

# --------------------
# DISPLAY CHAT HISTORY
# --------------------
for msg in st.session_state.chat_history[1:]:
    if msg["role"] == "user":
        st.markdown(
            f"<div style='background:#0e1117;padding:12px;border-radius:10px;text-align:right;'>"
            f"<b>You:</b> {msg['content']}"
            f"</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div style='background:#262730;padding:12px;border-radius:10px;'>"
            f"<b>MovieBot:</b> {msg['content']}"
            f"</div>",
            unsafe_allow_html=True
        )


