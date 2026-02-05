from src.vectorstore.base import VectorStore
from src.vectorstore.weaviate_client import get_weaviate_client

import weaviate.classes as wvc


class WeaviateStore(VectorStore):

    def __init__(self, config: dict):
        self.client = get_weaviate_client(config["url"])
        self.collection_name = config["class_name"]
        self.batch_size = config.get("batch_size", 32)

        self._ensure_collection()
        self.collection = self.client.collections.get(self.collection_name)

    def _ensure_collection(self):
        """
        Create collection if it does not exist.
        """
        if self.client.collections.exists(self.collection_name):
            return

        self.client.collections.create(
            name=self.collection_name,
            vectorizer_config=wvc.config.Configure.Vectorizer.none(),
            properties=[
                wvc.config.Property(
                    name="text",
                    data_type=wvc.config.DataType.TEXT
                ),
                wvc.config.Property(
                    name="source",
                    data_type=wvc.config.DataType.TEXT
                ),
                wvc.config.Property(
                    name="chunk_id",
                    data_type=wvc.config.DataType.INT
                ),
            ],
        )

    def upsert(self, texts, vectors, metadata):
        with self.collection.batch.dynamic() as batch:
            batch.batch_size = self.batch_size

            for text, vector, meta in zip(texts, vectors, metadata):
                batch.add_object(
                    properties={
                        "text": text,
                        "source": meta["source"],
                        "chunk_id": meta["chunk_id"],
                    },
                    vector=vector,
                )
