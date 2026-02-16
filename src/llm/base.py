from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseLLM(ABC):
    """
    Abstract base class for all LLM providers.
    RAG layer depends only on this contract.
    """

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Generate a completion from a plain text prompt.
        """
        pass

    @abstractmethod
    def chat(self, messages: List[Dict[str, str]]) -> str:
        """
        Generate a completion using chat-style messages.
        Example message format:
        [{"role": "system", "content": "..."}]
        """
        pass