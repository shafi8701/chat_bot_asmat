from src.chunking.base import BaseChunker

class OverlapChunker(BaseChunker):
    def __init__(self, chunk_size: int, overlap_size: int):
        self.chunk_size = chunk_size
        self.overlap_size = overlap_size

    def chunk(self, stream):
        buffer = ""
        for piece in stream:
            buffer += piece
            if len(buffer) >= self.chunk_size:
                yield buffer[:self.chunk_size].strip()
                buffer = buffer[self.chunk_size - self.overlap_size:]

        if buffer:
            yield buffer.strip()