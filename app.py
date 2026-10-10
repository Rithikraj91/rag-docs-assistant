import streamlit as st
import requests

st.set_page_config(page_title="Internal Docs Assistant", page_icon="🤖")

st.title("🤖 Internal Docs Assistant")
st.caption("Ask questions about internal platform runbooks and services.")

API_URL = "http://localhost:8000/query"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question about the docs..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching internal docs..."):
            try:
                response = requests.post(API_URL, json={"question": prompt}, timeout=60)
                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("answer", "No answer returned.")
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error(f"Error {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"Failed to connect to backend: {e}")
