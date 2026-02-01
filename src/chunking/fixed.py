from src.chunking.base import BaseChunker

class FixedChunker(BaseChunker):
    def __init__(self, chunk_size: int):
        self.chunk_size = chunk_size

    def chunk(self, stream):
        buffer = ""

        for piece in stream:
            buffer += piece

            if len(buffer) >= self.chunk_size:
                yield buffer.strip()
                buffer = ""

        if buffer:
            yield buffer.strip()