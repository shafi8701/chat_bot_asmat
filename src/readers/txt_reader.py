from typing import Iterator

def read_txt_stream(file_path) -> Iterator[str]:
    """Streams raw text line-by-line."""
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            yield line