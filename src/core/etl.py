import re
from src.readers.pdf_reader import read_pdf_stream
from src.readers.txt_reader import read_txt_stream
from src.chunking import get_chunker
from src.embeddings import get_embedder
from src.vectorstore import get_vector_store
from src.utils.file_utils import move_file


# Optional PRODUCT metadata extractor
PRODUCT_PATTERN = re.compile(r"^PRODUCT\s+([A-Z0-9 &\-]{3,})")

def extract_product_name(text: str) -> str | None:
    match = PRODUCT_PATTERN.match(text.strip())
    return match.group(1).strip() if match else None


def process_file(file_path, processed_dir):
    suffix = file_path.suffix.lower()

    print("START: ETL Run")

    if suffix == ".pdf":
        print("START: Reading PDF Data. Page Wise.")
        reader_stream = read_pdf_stream(file_path)
        print("END: Reading PDF Data. Page Wise.")
    elif suffix == ".txt":
        reader_stream = read_txt_stream(file_path)
    else:
        print(f"⚠️ Unsupported file: {file_path.name}")
        return

    chunker = get_chunker()
    embedder = get_embedder()
    vector_store = get_vector_store()

    # 🔹 Chunking
    chunks = list(chunker.chunk(reader_stream))

    if not chunks:
        print("⚠️ No chunks generated.")
        return

    print(f"Total chunks generated: {len(chunks)}")

    # 🔥 ONE batch embedding
    vectors = embedder.embed_batch(chunks)

    # 🔹 Metadata enrichment (OPTIONAL product extraction)
    metadata = []

    for idx, chunk in enumerate(chunks, start=1):

        base_meta = {
            "source": file_path.name,
            "chunk_id": idx,
        }

        product_name = extract_product_name(chunk)

        # Add only if present
        if product_name:
            base_meta["product_name"] = product_name

        metadata.append(base_meta)

    # 🔥 ONE batch upsert
    print("Update/Insert into vector DB.")
    vector_store.upsert(
        texts=chunks,
        vectors=vectors,
        metadata=metadata,
    )
    print("Update/Insert into vector DB complete.")

    #vector_store.getAllDocuments()

    #vector_store.keywordSearch("Bakhoor")

    user_query = "Arabic Perfume"
    user_query_vector = embedder.embed(user_query)
    vector_store.semanticSearch(user_query_vector)

    # move_file(file_path, processed_dir / file_path.name)