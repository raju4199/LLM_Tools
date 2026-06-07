"""
Groq Connector - Free API, no model download needed
Supports: llama3-8b-8192, llama3-70b-8192, mixtral-8x7b-32768, gemma-7b-it
Sign up free at: https://console.groq.com
"""

import requests

class GroqConnector:
    BASE_URL = "https://api.groq.com/openai/v1/chat/completions"

    def __init__(self, api_key, model="llama3-8b-8192"):
        self.api_key = api_key
        self.model = model
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def send(self, prompt, system_prompt=None):
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": 512,
            "temperature": 0
        }

        try:
            response = requests.post(
                self.BASE_URL,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            data = response.json()
            if "choices" in data:
                return data["choices"][0]["message"]["content"]
            elif "error" in data:
                return f"ERROR: {data['error']['message']}"
            return str(data)
        except Exception as e:
            return f"ERROR: {str(e)}"
