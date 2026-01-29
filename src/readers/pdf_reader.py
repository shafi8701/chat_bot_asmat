from pypdf import PdfReader

def read_pdf(file_path):
    reader = PdfReader(file_path)
    content = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            content.append(text)

    return "\n".join(content)