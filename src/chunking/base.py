from abc import ABC, abstractmethod
from typing import Iterator

class BaseChunker(ABC):
    @abstractmethod
    def chunk(self, text: str) -> Iterator[str]:
        pass