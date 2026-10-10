import streamlit as st
import requests

st.set_page_config(page_title="Internal Docs Assistant", page_icon="🤖")

st.title("🤖 Internal Docs Assistant")
st.caption("RAG-powered assistant answering questions from internal runbooks.")

# FastAPI backend endpoint
API_URL = "http://localhost:8001/query"

# Maintain chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display prior chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "context" in msg and msg["context"]:
            with st.expander("Retrieved Context"):
                st.code(msg["context"])

# User query input
if prompt := st.chat_input("Ask a question about the internal documentation..."):
    # Render user prompt
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Request response from FastAPI service
    with st.chat_message("assistant"):
        with st.spinner("Searching docs and generating response..."):
            try:
                res = requests.post(API_URL, json={"question": prompt}, timeout=60)
                if res.status_code == 200:
                    data = res.json()
                    answer = data.get("answer", "No answer returned.")
                    context = data.get("context", "")

                    st.markdown(answer)
                    if context:
                        with st.expander("Retrieved Context"):
                            st.code(context)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "context": context
                    })
                else:
                    err_msg = f"API Error ({res.status_code}): {res.text}"
                    st.error(err_msg)
            except Exception as e:
                st.error(f"Failed to connect to backend: {e}")
