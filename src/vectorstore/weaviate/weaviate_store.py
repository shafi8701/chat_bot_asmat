from src.vectorstore.base import VectorStore
from src.vectorstore.weaviate.weaviate_client import get_weaviate_client


import weaviate.classes as wvc

#Needed for deterministic uuid function...
import uuid
import hashlib

class WeaviateStore(VectorStore):

    def __init__(self, config: dict):
        self.client = get_weaviate_client(config["url"])
        self.collection_name = config["class_name"]
        self.batch_size = config.get("batch_size", 32)

        self._ensure_collection()
        self.collection = self.client.collections.get(self.collection_name)

    ##Helper functions for the DB... 
    ###Start
    def _exists(self, uid: str) -> bool:
        try:
            obj = self.collection.query.fetch_object_by_id(uid)
            # If it returns without error and has an object, it exists
            return obj is not None and getattr(obj, "uuid", None) is not None
        except Exception:
            return False

    @staticmethod
    def deterministic_uuid(source: str, chunk_id: int, text: str | None = None) -> str:
        """
        Deterministically generate a UUID for a chunk using uuid5.
        - Stable across runs: same inputs -> same UUID.
        - Namespace is fixed (NAMESPACE_URL), key is your domain-specific string.
        - Optionally include a short hash of text to guard against accidental collisions
        when (source, chunk_id) might repeat with different content.
        """
        key = f"{source}:{chunk_id}"
        if text is not None:
            # Short, stable content fingerprint (avoid storing full text in the key)
            h = hashlib.sha1(text.strip().encode("utf-8")).hexdigest()[:16]
            key = f"{key}:{h}"

        return str(uuid.uuid5(uuid.NAMESPACE_URL, key))

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

    ##Helper functions for the DB... 
    ###End


    ##Interface functions...... 
    ###Start
    """
    This is for testing and practice purpose... 
    Just fetch all the documents in the class...
    """
    def getAllDocuments(self):
        result = self.collection.query.fetch_objects()

        items = []
        for obj in getattr(result, "objects", []) or []:
            props = getattr(obj, "properties", {}) or {}
            items.append({
                "id": getattr(obj, "uuid", None) or getattr(obj, "id", None),
                "text": props.get("text"),
                "source": props.get("source"),
                "chunk_id": props.get("chunk_id"),
            })

        for it in items:
            print(f"Document Object: {it}")

        return items

    def upsert(self, texts, vectors, metadata):
        assert len(texts) == len(vectors) == len(metadata)

        for text, vector, meta in zip(texts, vectors, metadata):
            src = meta["source"]
            cid = meta["chunk_id"]
            uid = self.deterministic_uuid(src, cid, text=str(text))

            if self._exists(uid):
                # full replace semantics
                self.collection.data.replace(
                    uuid=uid,
                    properties={
                        "text": text,
                        "source": src,
                        "chunk_id": cid,
                    },
                    vector=vector,
                )
            else:
                self.collection.data.insert(
                    properties={
                        "text": text,
                        "source": src,
                        "chunk_id": cid,
                    },
                    uuid=uid,
                    vector=vector,
                )
    
    ##Interface functions...... 
    ###End

    def keywordSearch(self, query: str, limit: int = 5):
        """
        Perform BM25 keyword search on the 'text' field.
        """
        response = self.collection.query.bm25(
            query=query,
            query_properties=["text"],  # search only inside text field
            limit=limit
            return_metadata=wvc.query.MetadataQuery(score=True)
        )

        results = []
        for obj in getattr(response, "objects", []) or []:
            props = getattr(obj, "properties", {}) or {}

            results.append({
                "id": getattr(obj, "uuid", None),
                "text": props.get("text"),
                "source": props.get("source"),
                "chunk_id": props.get("chunk_id"),
            })

        for obj in results:
            print(f"Document Object: {obj}")

        return results