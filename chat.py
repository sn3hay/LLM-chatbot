import streamlit as st
from data_handler import extract_text_from_pdf, store_text_in_chroma, retrieve_relevant_text
from ollama_query import query_ollama

st.title("LLM RAG Chatbot")

# Load and index the PDF on startup
try:
    pdf_text = extract_text_from_pdf()
    store_text_in_chroma(pdf_text)
    st.success("PDF loaded from directory and indexed successfully!")
except FileNotFoundError as e:
    st.error(str(e))

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Ask something about the PDF..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Retrieve relevant text from ChromaDB
    relevant_context = retrieve_relevant_text(prompt)

    # Query Ollama with retrieved context
    assistant_response = query_ollama(prompt, relevant_context)

    with st.chat_message("assistant"):
        st.markdown(assistant_response)

    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
