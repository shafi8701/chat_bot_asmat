from src.readers.pdf_reader import read_pdf
from src.readers.txt_reader import read_txt
from src.writers.printer import print_content
from src.utils.file_utils import move_file

def process_file(file_path, processed_dir):
    suffix = file_path.suffix.lower()


    if suffix == ".pdf":
        content = read_pdf(file_path)
    elif suffix == ".txt":
        content = read_txt(file_path)
    else:
        print(f"⚠️ Unsupported file: {file_path.name}")
        return

    print_content(file_path.name, content)
    move_file(file_path, processed_dir / file_path.name)