import requests

class GenericHTTPConnector:
    def __init__(self, url, headers=None):
        self.url = url
        self.headers = headers or {"Content-Type": "application/json"}

    def send(self, prompt, system_prompt=None):
        payload = {"message": prompt}
        if system_prompt:
            payload["system"] = system_prompt

        try:
            response = requests.post(self.url, json=payload, headers=self.headers, timeout=30)
            data = response.json()
            # Try common response keys
            for key in ["response", "message", "content", "text", "output"]:
                if key in data:
                    return data[key]
            return str(data)
        except Exception as e:
            return f"ERROR: {str(e)}"
