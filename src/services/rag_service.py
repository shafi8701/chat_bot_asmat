# src/services/rag_service.py

from src.embeddings import get_embedder
from src.vectorstore import get_vector_store
from src.llm import get_llm  # assuming you have this

class RAGService:

    def __init__(self):
        self.embedder = get_embedder()
        self.vector_store = get_vector_store()
        self.llm = get_llm()

    def retrieve(self, query: str, top_k: int = 5):
        # 1️⃣ Embed user query
        query_vector = self.embedder.embed(query)

        # 2️⃣ Hybrid search
        results = self.vector_store.hybridSearch(
            query,
            query_vector,
            top_k=top_k
        )

        return results

    def generate(self, query: str):
        # 1️⃣ Retrieve documents
        docs = self.retrieve(query)

        # 2️⃣ Build context
        context = "\n\n".join(
            doc["text"] for doc in docs
        )

        # 3️⃣ Build prompt
        prompt = f"""
        Answer the question using the context below.

        Context:
        {context}

        Question:
        {query}
        """

        # 4️⃣ Call LLM
        response = self.llm.generate(prompt)

        return response