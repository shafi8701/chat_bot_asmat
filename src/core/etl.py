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

    chunker = get_chunker()
    
    embedder = get_embedder()
    
    vector_store = get_vector_store()
    
    chunks = list(chunker.chunk(reader_stream))
    

    if not chunks:
        return

    # 🔥 ONE batch embedding
    
    vectors = embedder.embed_batch(chunks)
    
    metadata = [
        {
            "source": file_path.name,
            "chunk_id": idx,
        }
        for idx, chunk in enumerate(chunks, start=1)
    ]
   

    # 🔥 ONE batch upsert

    print(f"Update/Insert into vector DB.")
    vector_store.upsert(
        texts=chunks,
        vectors=vectors,
        metadata=metadata,
    )
    print(f"Update/Insert into vector DB complete.")

    print(f"Fetching all the documents.")

    vector_store.getAllDocuments()

    #move_file(file_path, processed_dir / file_path.name)
