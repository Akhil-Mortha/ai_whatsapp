import streamlit as st
import requests

# ✅ LOCAL backend
BACKEND_URL = "http://127.0.0.1:8000/chat"

st.set_page_config(page_title="AI Chat", page_icon="🤖")

# Session
if "user" not in st.session_state:
    st.session_state.user = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# 🔐 Login
if not st.session_state.user:
    st.title("🔐 Login")

    username = st.text_input("Username")

    if st.button("Login"):
        if username.strip():
            st.session_state.user = username
            st.rerun()
        else:
            st.warning("Enter username")

# 🤖 Chat
else:
    st.title(f"🤖 AI Chat ({st.session_state.user})")

    if st.button("Logout"):
        st.session_state.user = None
        st.session_state.messages = []
        st.rerun()

    # Show history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("Type your message...")

    if user_input:
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        with st.chat_message("user"):
            st.write(user_input)

        try:
            with st.spinner("Thinking..."):
                response = requests.post(
                    BACKEND_URL,
                    json={
                        "message": user_input,
                        "user_id": st.session_state.user
                    },
                    timeout=30
                )

            if response.status_code == 200:
                ai_reply = response.json()["response"]
            else:
                ai_reply = f"❌ Backend error: {response.status_code}"

        except Exception as e:
            ai_reply = f"❌ Error: {e}"

        st.session_state.messages.append({
            "role": "assistant",
            "content": ai_reply
        })

        with st.chat_message("assistant"):
            st.write(ai_reply)
