from src.readers.pdf_reader import read_pdf_stream
from src.readers.txt_reader import read_txt_stream
from src.chunking import get_chunker
from src.embeddings import get_embedder
from src.vectorstore import get_vector_store
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
    embedder = get_embedder()
    vector_store = get_vector_store()

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
    vector_store.upsert(
        texts=texts,
        vectors=vectors,
        metadata=metadata,
    )

    move_file(file_path, processed_dir / file_path.name)
