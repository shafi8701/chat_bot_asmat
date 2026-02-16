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

    @abstractmethod
    def getAllDocuments(
        self
    ):
        pass

    @abstractmethod
    def keywordSearch(
        self,
        query
    ):
        pass
    
    @abstractmethod
    def semanticSearch(
        self,
        query_vector
    ):
        pass
    
    @abstractmethod
    def hybridSearch(
        self,
        query,
        query_vector
    ):
        pass