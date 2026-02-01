from src.chunking.base import BaseChunker

class ParagraphChunker(BaseChunker):
    def __init__(self, min_length: int, max_length: int):
        self.min = min_length
        self.max = max_length

    def chunk(self, text: str):
        buffer = ""
        for para in text.split("\n\n"):
            if len(buffer) + len(para) <= self.max:
                buffer += para + "\n\n"
            else:
                if len(buffer) >= self.min:
                    yield buffer.strip()
                buffer = para + "\n\n"
            
            if buffer:
                yield buffer.strip()