import re
from src.chunking.base import BaseChunker


class SectionChunker(BaseChunker):

    _PRODUCT_RE = re.compile(
        r"(?m)^PRODUCT\s+[A-Z0-9 &\-]{3,}\s*$"
    )

    def __init__(self, min_length: int = None, max_length: int = None):
        # Accept args for compatibility, even if unused
        self.min_length = min_length
        self.max_length = max_length

    def chunk(self, stream):

        if isinstance(stream, str):
            stream = iter([stream])

        full_text = "".join(stream)
        full_text = full_text.replace("\r\n", "\n").replace("\r", "\n")

        matches = list(self._PRODUCT_RE.finditer(full_text))

        if not matches:
            return

        for i in range(len(matches)):
            start = matches[i].start()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(full_text)

            section = full_text[start:end].strip()

            if section:
                yield section