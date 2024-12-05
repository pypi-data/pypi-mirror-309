import subprocess
import time

def ensure_ollama_models():
    models = ["llama2:3b", "nomic-embed-text:latest"]
    for model in models:
        try:
            subprocess.run(["ollama", "pull", model], check=True)
        except subprocess.CalledProcessError:
            print(f"Failed to pull {model}. Please ensure Ollama is installed and running.")
            time.sleep(2)  # Give some time for the error message to be read
