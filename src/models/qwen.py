from openai import AsyncOpenAI

from base_model import Model

class Qwen (Model):
    def __init__(self):
        self.messages = [
            {"role": "system", "content": "You are an expert Coq programmer"}
        ]
        self.client = AsyncOpenAI(
                        api_key="EMPTY",
                        base_url="http://localhost:2731/v1"
        )
    
    async def send (self, message: str) -> str:
        self.messages.append (
            {"role": "user", "content": message}
        )
        result = (await self.client.chat.completions.create(
            model="Qwen/Qwen3-8B",
            messages=self.messages,
        )).choices[0].message.content or ""
        self.messages.append(
            {"role": "assistant", "content": result}
        )
        return result

    def clear_history(self):
        self.messages = []
