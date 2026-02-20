import requests
import json

def verify_ollama_connection(model_name="codellama"):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model_name,
        "prompt": "ping",
        "stream": False
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        if response.status_code == 200:
            print(f"Successfully connected to {model_name}")
            return True
        else:
            print(f"Failed to connect to {model_name}. Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error connecting to Ollama: {str(e)}")
        return False

if __name__ == "__main__":
    verify_ollama_connection()
