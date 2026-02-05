from src.vectorstore.base import VectorStore
from src.vectorstore.weaviate_client import get_weaviate_client

class WeaviateStore(VectorStore):

    def __init__(self, config: dict):
        self.client = get_weaviate_client(config["url"])
        self.class_name = config["class_name"]
        self.batch_size = config.get("batch_size", 32)

    def upsert(self, texts, vectors, metadata):
        with self.client.batch as batch:
            batch.batch_size = self.batch_size
            for text, vector, meta in zip(texts, vectors, metadata):
                batch.add_data_object(
                    {
                        "text": text,
                        "source": meta["source"],
                        "chunk_id": meta["chunk_id"],
                    },
                    class_name=self.class_name,
                    vector=vector,
                )