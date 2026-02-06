# Global chunking object to ensure singleton class structure is followed...
_chunking = None


# src/chunking/factory.py
from src.chunking.fixed import FixedChunker
from src.chunking.overlap import OverlapChunker
from src.chunking.paragraph import ParagraphChunker
from src.config import get_chunking_method, CONFIG

#YAML convert to readable json config...
import yaml
from pathlib import Path
_CONFIG_PATH = Path("src/config/chunking.yaml")

def _load_config():
    with open(_CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)

def get_chunking_method():
    return CONFIG["chunking"]["method"]

def get_chunker():
    """
    Factory method:
    - Loads YAML once
    - Instantiates correct chunking service
    - Returns singleton
    """

    global _chunking

    if _chunking is not None:
        return _chunking
    
    config = _load_config();
    method = get_chunking_method()

    if method == "fixed":
        cfg = CONFIG["fixed"]
        _chunking = FixedChunker(cfg["chunk_size"])

    if method == "overlap":
        cfg = CONFIG["overlap"]
        _chunking = OverlapChunker(cfg["chunk_size"], cfg["overlap_size"])

    if method == "paragraph":
        cfg = CONFIG["paragraph"]
        _chunking = ParagraphChunker(cfg["min_length"], cfg["max_length"])
    else:
        raise ValueError(f"Unsupported chunking method: {method}")
    
    return _chunking