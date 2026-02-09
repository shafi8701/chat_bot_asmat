from src.chunking.base import BaseChunker

class FixedChunker(BaseChunker):
    def __init__(self, chunk_size: int):
        if chunk_size <= 0:
            raise ValueError("chunk_size must be > 0")
        self.chunk_size = chunk_size

    def chunk(self, stream):
        buffer = ""

        for piece in stream:
            buffer += piece

            # Keep emitting fixed-size chunks as long as possible
            while len(buffer) >= self.chunk_size:
                yield buffer[:self.chunk_size].strip()
                buffer = buffer[self.chunk_size:]

        # Emit the final remainder (if any)
        if buffer.strip():
            yield buffer.strip()