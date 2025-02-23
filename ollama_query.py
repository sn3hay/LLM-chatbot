import requests
import json

OLLAMA_SERVER_URL = "http://localhost:11434/api/generate"

def query_ollama(user_query, context):
    """Queries the local Ollama model with relevant context."""
    full_prompt = f"Context: {context}\n\nUser Query: {user_query}"

    payload = {
        "model": "llama3.2",
        "prompt": full_prompt,
        "messages": [{"role": "user", "content": user_query}]
    }

    try:
        response = requests.post(OLLAMA_SERVER_URL, json=payload)
        response.raise_for_status()
        response_parts = response.text.strip().split('\n')

        assistant_response = ""
        for part in response_parts:
            try:
                data = json.loads(part)
                assistant_response += data.get("response", "")
                if data.get("done"):
                    break
            except json.JSONDecodeError:
                pass

        return assistant_response
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"
