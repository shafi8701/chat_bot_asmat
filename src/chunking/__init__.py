from src.chunking.fixed import FixedChunker
from src.chunking.overlap import OverlapChunker
from src.chunking.paragraph import ParagraphChunker
from src.config import CHUNKING_CONFIG


def get_chunker():
    method = CHUNKING_CONFIG["method"]

    if method == "fixed":
        cfg = CHUNKING_CONFIG["fixed"]
        return FixedChunker(cfg["chunk_size"])

    if method == "overlap":
        cfg = CHUNKING_CONFIG["overlap"]
        return OverlapChunker(cfg["chunk_size"], cfg["overlap_size"])


    if method == "paragraph":
        cfg = CHUNKING_CONFIG["paragraph"]
        return ParagraphChunker(cfg["min_length"], cfg["max_length"])

    raise ValueError(f"Unknown chunking method: {method}")