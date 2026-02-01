from src.readers.pdf_reader import read_pdf_stream
from src.readers.txt_reader import read_txt_stream
from src.chunking import get_chunker
from src.writers.printer import print_content
from src.utils.file_utils import move_file


def process_file(file_path, processed_dir):
    suffix = file_path.suffix.lower()

    if suffix == ".pdf":
        reader_stream = read_pdf_stream(file_path)
    elif suffix == ".txt":
        reader_stream = read_txt_stream(file_path)
    else:
        print(f"⚠️ Unsupported file: {file_path.name}")
        return

    chunker = get_chunker()

    for idx, chunk in enumerate(chunker.chunk(reader_stream), start=1):
        print_content(
            filename=f"{file_path.name} | chunk {idx}",
            content=chunk
        )

    move_file(file_path, processed_dir / file_path.name)