import yaml
from pathlib import Path
from src.embeddings.bge import BGEEmbeddingService

_CONFIG_PATH = Path("src/config/embedding.yaml")

_embedder = None

def _load_config():
    with open(_CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


def get_embedder():
    """
    Factory method:
    - Loads YAML once
    - Instantiates correct embedding service
    - Returns singleton
    """
    global _embedder

    if _embedder is not None:
        return _embedder

    config = _load_config()
    embed_type = config.get("type")

    if embed_type == "bge":
        _embedder = BGEEmbeddingService(config["bge"])
    else:
        raise ValueError(f"Unsupported embedding type: {embed_type}")

    return _embedder