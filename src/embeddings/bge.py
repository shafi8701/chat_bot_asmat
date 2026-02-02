from sentence_transformers import SentenceTransformer
from typing import List


class BGEEmbeddingService:
    _model = None

    def __init__(self, config: dict):
        if BGEEmbeddingService._model is None:
            print(f"🧠 Loading BGE model: {config['model_name']}")

            BGEEmbeddingService._model = SentenceTransformer(
                config["model_name"],
                device=config.get("device", "cpu")
            )

        self.normalize = config.get("normalize", True)
        self.batch_size = config.get("batch_size", 16)

    def embed(self, text: str) -> List[float]:
        vec = BGEEmbeddingService._model.encode(
            text,
            normalize_embeddings=self.normalize
        )
        print(f"🧠 Embedding text complete.")
        return vec.tolist()

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        vecs = BGEEmbeddingService._model.encode(
            texts,
            batch_size=self.batch_size,
            normalize_embeddings=self.normalize
        )
        return vecs.tolist()