from abc import ABC, abstractmethod
from typing import List, Dict

class VectorStore(ABC):

    @abstractmethod
    def upsert(
        self,
        texts: List[str],
        vectors: List[List[float]],
        metadata: List[Dict]
    ):
        pass

    def getAllDocuments(
        self
    ):
        pass

    def keawordSearch(
        self
    ):
        pass