from typing import Iterator, Union
import re
from src.chunking.base import BaseChunker


class ParagraphChunker(BaseChunker):
    """
    Stream-based paragraph chunker.

    Input:
      - stream: Iterator[str] (e.g., PDF pages from read_pdf_stream)

    Behavior:
      - Splits incoming text into paragraphs (blank-line separated)
      - Accumulates paragraphs into a buffer
      - Emits a chunk when adding the next paragraph would exceed max_length
      - Ensures chunks are ideally >= min_length (but will emit smaller tail at end)
      - Splits overly long paragraphs (> max_length) into max_length pieces
    """

    _PARA_SPLIT_RE = re.compile(r"\n\s*\n+")  # one or more blank lines

    def __init__(self, min_length: int, max_length: int, reset_on_page: bool = False):
        if min_length <= 0 or max_length <= 0:
            raise ValueError("min_length and max_length must be > 0")
        if min_length > max_length:
            raise ValueError("min_length must be <= max_length")

        self.min = min_length
        self.max = max_length
        self.reset_on_page = reset_on_page

    def _normalize(self, s: str) -> str:
        """
        Light normalization suitable for PDF text:
        - normalize line endings
        - collapse 3+ newlines into 2 newlines (keeps paragraph breaks)
        """
        s = (s or "").replace("\r\n", "\n").replace("\r", "\n")
        s = re.sub(r"\n{3,}", "\n\n", s)
        return s

    def _iter_paragraphs(self, text: str) -> Iterator[str]:
        """
        Split text into paragraphs. A paragraph is a block separated by blank lines.
        """
        text = self._normalize(text).strip()
        if not text:
            return
        for para in self._PARA_SPLIT_RE.split(text):
            para = para.strip()
            if para:
                yield para

    def _split_long(self, para: str) -> Iterator[str]:
        """
        If a single paragraph is longer than max_length, split it into max_length slices.
        (You can later upgrade this to sentence-aware splitting if needed.)
        """
        start = 0
        n = len(para)
        while start < n:
            yield para[start:start + self.max].strip()
            start += self.max

    def chunk(self, stream: Union[Iterator[str], str]) -> Iterator[str]:
        """
        Chunk a stream (generator) of text pieces into paragraph-based chunks.
        If caller accidentally passes a single string, we treat it as a one-item stream.
        """
        if isinstance(stream, str):
            stream = iter([stream])

        buffer = ""

        def flush():
            nonlocal buffer
            out = buffer.strip()
            buffer = ""
            if out:
                return out
            return None

        for piece in stream:
            if self.reset_on_page and buffer.strip():
                # if you want strict page-local chunks, flush at page boundary
                out = flush()
                if out:
                    yield out

            for para in self._iter_paragraphs(piece):
                # Handle huge paragraphs
                if len(para) > self.max:
                    # Flush whatever we have accumulated first
                    out = flush()
                    if out:
                        yield out
                    # Emit the long paragraph in max-sized pieces
                    yield from self._split_long(para)
                    continue

                # Candidate buffer if we add this paragraph
                candidate = para if not buffer else f"{buffer}\n\n{para}"

                if len(candidate) <= self.max:
                    buffer = candidate
                else:
                    # Buffer would overflow; emit current buffer
                    out = flush()
                    if out:
                        yield out
                    # Start new buffer with current paragraph
                    buffer = para

        # Emit remaining tail
        if buffer.strip():
            yield buffer.strip()