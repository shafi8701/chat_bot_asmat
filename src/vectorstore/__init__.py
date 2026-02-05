import yaml
from pathlib import Path

from src.vectorstore.weaviate_store import WeaviateStore

_VECTOR_STORE = None

def get_vector_store():
    global _VECTOR_STORE

    if _VECTOR_STORE is not None:
        return _VECTOR_STORE

    config_path = Path(__file__).parents[1] / "config" / "vectorstore.yml"
    with open(config_path) as f:
        config = yaml.safe_load(f)

    backend = config["backend"]

    if backend == "weaviate":
        _VECTOR_STORE = WeaviateStore(config["weaviate"])
    else:
        raise ValueError(f"Unsupported vector DB: {backend}")

    return _VECTOR_STORE