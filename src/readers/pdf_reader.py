from pypdf import PdfReader
from typing import Iterator

def read_pdf_stream(file_path) -> Iterator[str]:
    """
    Streams raw text from PDF page-by-page.
    NO chunking happens here.
    """
    reader = PdfReader(file_path)
    
    for page_num, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        yield text