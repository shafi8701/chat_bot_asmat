from src.chunking.base import BaseChunker

class OverlapChunker(BaseChunker):
    def __init__(self, chunk_size: int, overlap_size: int):
        if overlap_size < 0 or overlap_size >= chunk_size:
            raise ValueError("overlap_size must be >= 0 and < chunk_size")

        self.chunk_size = chunk_size
        self.overlap_size = overlap_size

    def chunk(self, stream):
        buffer = ""
        step = self.chunk_size - self.overlap_size

        for piece in stream:
            buffer += piece

            # IMPORTANT: emit as many chunks as possible
            while len(buffer) >= self.chunk_size:
                yield buffer[:self.chunk_size].strip()
                buffer = buffer[step:]

        if buffer.strip():
            yield buffer.strip()