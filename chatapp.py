import streamlit as st
import openai

openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("🎬 MovieBot")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "system",
            "content": "You are MovieBot, a funny and friendly AI who loves movies."
        }
    ]

for msg in st.session_state.chat_history[1:]:
    st.chat_message(msg["role"]).write(msg["content"])

user_input = st.chat_input("Ask MovieBot something...")

if user_input:
    st.session_state.chat_history.append(
        {"role": "user", "content": user_input}
    )

    response = openai.ChatCompletion.create(
        model="gpt-5-mini",
        messages=st.session_state.chat_history
    )

    reply = response["choices"][0]["message"]["content"]

    st.session_state.chat_history.append(
        {"role": "assistant", "content": reply}
    )

    st.chat_message("assistant").write(reply)
