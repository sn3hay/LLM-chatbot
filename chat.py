import streamlit as st
import requests  # This will be used to send requests to the Ollama API
import json  # To handle the multiple JSON objects

st.title("LLM-chatbot")

# Define the URL for Ollama's local server
OLLAMA_SERVER_URL = "http://localhost:11434/api/generate"  # Replace with the correct URL if necessary

if "llama_model" not in st.session_state:
    st.session_state["llama_model"] = "llama3.2"  # Use "llama3.2" as the model name

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input field for the user to enter their message
if prompt := st.chat_input("What is up?"):
    # Add the user's message to the session state
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user's message in the chat
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare the payload for the request to Ollama's server
    payload = {
        "model": st.session_state["llama_model"],  # The model you want to use, e.g., "llama3.2"
        "prompt": prompt,
        "messages": [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]
    }

    # Send the request to the Ollama server to get a response from the model
    try:
        response = requests.post(OLLAMA_SERVER_URL, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP error responses

        # Debug: print the raw response
        st.write("Raw response:", response.text)  # This will show the raw response content

        # Split the response into multiple JSON objects
        response_parts = response.text.strip().split('\n')

        # Initialize an empty string to collect the final response
        assistant_response = ""

        # Parse and combine each part of the response
        for part in response_parts:
            try:
                data = json.loads(part)
                assistant_response += data.get("response", "")
                if data.get("done"):
                    break  # Stop when the response is complete
            except json.JSONDecodeError:
                st.write(f"Error parsing part of the response: {part}")

    except requests.exceptions.RequestException as e:
        # Handle other HTTP-related errors (e.g., connection issues)
        assistant_response = f"Error: {e}"
    except requests.exceptions.JSONDecodeError:
        # Handle case where the response is not valid JSON
        assistant_response = f"Error: Invalid JSON response from the server. Response: {response.text}"

    # Display the assistant's response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)

    # Add the assistant's message to the session state
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
