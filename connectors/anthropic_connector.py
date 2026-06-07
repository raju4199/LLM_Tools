import anthropic

class AnthropicConnector:
    def __init__(self, api_key, model="claude-3-haiku-20240307"):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    def send(self, prompt, system_prompt=None):
        kwargs = {
            "model": self.model,
            "max_tokens": 512,
            "messages": [{"role": "user", "content": prompt}]
        }
        if system_prompt:
            kwargs["system"] = system_prompt

        try:
            response = self.client.messages.create(**kwargs)
            return response.content[0].text
        except Exception as e:
            return f"ERROR: {str(e)}"
