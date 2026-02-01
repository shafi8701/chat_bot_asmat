# src/chunking/factory.py
from src.chunking.fixed import FixedChunker
from src.chunking.overlap import OverlapChunker
from src.chunking.paragraph import ParagraphChunker
from src.config import get_chunking_method, CONFIG

def get_chunker():
    method = get_chunking_method()

    if method == "fixed":
        cfg = CONFIG["fixed"]
        return FixedChunker(cfg["chunk_size"])

    if method == "overlap":
        cfg = CONFIG["overlap"]
        return OverlapChunker(cfg["chunk_size"], cfg["overlap_size"])

    if method == "paragraph":
        cfg = CONFIG["paragraph"]
        return ParagraphChunker(cfg["min_length"], cfg["max_length"])

    raise ValueError(f"Unknown chunking method: {method}")