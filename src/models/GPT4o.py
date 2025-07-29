from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

from models.base_model import Model

class GPT4o (Model):
    def __init__(self):
        self.messages = [
            {"role": "system", "content": "You are an expert Lean4 programmer"}
        ]
        self.client = AsyncOpenAI()
    
    async def send (self, message: str) -> str:
        self.messages.append (
            {"role": "user", "content": message}
        )
        result = (await self.client.chat.completions.create(
            model="gpt-4o",
            messages=self.messages,
        )).choices[0].message.content or ""
        self.messages.append(
            {"role": "assistant", "content": result}
        )
        return result

    def clear_history(self):
        self.messages = []
