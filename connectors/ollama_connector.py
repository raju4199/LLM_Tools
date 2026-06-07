import requests
import sys

class OllamaConnector:
    def __init__(self, model="llama3", base_url="http://localhost:11434"):
        self.model = model
        self.base_url = base_url
        self._check_connection()

    def _check_connection(self):
        try:
            r = requests.get(f"{self.base_url}", timeout=5)
            if r.status_code != 200:
                self._abort()
        except Exception:
            self._abort()

    def _abort(self):
        print("\n[ERROR] Ollama server not running!")
        print("  Fix: Run 'ollama serve' in a separate terminal")
        print("  Then re-run llmscan\n")
        sys.exit(1)

    def send(self, prompt, system_prompt=None):
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        if system_prompt:
            payload["system"] = system_prompt

        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=60
            )
            return response.json().get("response", "")
        except Exception as e:
            return f"ERROR: {str(e)}"
