from openai import OpenAI
from typing import List, Dict
from src.llm.base import BaseLLM

class OpenAILLM(BaseLLM):

    def __init__(self, api_key: str, model: str, temperature: int):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
        )

        return response.choices[0].message.content

    def chat(self, messages: List[Dict[str, str]]) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
        )

        return response.choices[0].message.content