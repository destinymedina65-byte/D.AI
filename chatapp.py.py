import streamlit as st
from openai import OpenAI

client = OpenAI()

st.title("💬 MovieBot")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "system",
            "content": "You are MovieBot, a funny and friendly AI who loves movies."
        }
    ]

user_input = st.text_input("You:")

if user_input:
    st.session_state.chat_history.append(
        {"role": "user", "content": user_input}
    )

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=st.session_state.chat_history
    )

    reply = response.choices[0].message.content

    st.session_state.chat_history.append(
        {"role": "assistant", "content": reply}
    )

for msg in st.session_state.chat_history[1:]:
    st.write(f"**{msg['role'].capitalize()}:** {msg['content']}")
