from src.readers.pdf_reader import read_pdf_stream
from src.readers.txt_reader import read_txt_stream
from src.chunking import get_chunker
from src.embeddings import get_embedder
from src.vectorstore import get_vector_store
from src.utils.file_utils import move_file


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

    print(f"PDF Data Stream: {reader_stream}")

    print(f"START: Creating chunking object")
    chunker = get_chunker()
    print(f"END: Creating chunking object")
    
    print(f"START: Creating Embedding object")
    embedder = get_embedder()
    print(f"END: Creating Embedding object")
    
    print(f"START: Creating Vector Store object")
    #vector_store = get_vector_store()
    print(f"END: Creating Vector Store object")

    chunks = list(chunker.chunk(reader_stream))
    if not chunks:
        return

    texts = [chunk.text for chunk in chunks]
    metadata = [
        {
            "source": file_path.name,
            "chunk_id": idx,
            **chunk.metadata,
        }
        for idx, chunk in enumerate(chunks, start=1)
    ]

    # 🔥 ONE batch embedding
    vectors = embedder.embed_batch(texts)

    # 🔥 ONE batch upsert
    #vector_store.upsert(
    #    texts=texts,
    #    vectors=vectors,
    #    metadata=metadata,
    #)

    move_file(file_path, processed_dir / file_path.name)
