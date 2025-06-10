import requests

OLLAMA_URL = "http://ollama:11434/api/generate"
MODEL = "llama4"

def generate_completion(prompt):
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()
    return response.json()["response"] 