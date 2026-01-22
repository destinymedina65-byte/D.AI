import streamlit as st
from openai import OpenAI, RateLimitError

client = OpenAI()

st.title("💬 MovieBot")

# Initialize chat memory
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "system",
            "content": "You are MovieBot, a funny and friendly AI who loves movies."
        }
    ]

# Chat input (prevents multiple API calls)
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("You:")
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    st.session_state.chat_history.append(
        {"role": "user", "content": user_input}
    )

    # Limit history to prevent rate limits
    st.session_state.chat_history = (
        st.session_state.chat_history[:1]
        + st.session_state.chat_history[-10:]
    )

    try:
        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=st.session_state.chat_history
        )
        reply = response.choices[0].message.content
    except RateLimitError:
        reply = "⏳ I'm being rate-limited. Please wait a moment and try again."

    st.session_state.chat_history.append(
        {"role": "assistant", "content": reply}
    )

# Display conversation
for msg in st.session_state.chat_history[1:]:
    st.write(f"**{msg['role'].capitalize()}:** {msg['content']}")
