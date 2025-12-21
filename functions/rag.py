class RagPipeline:
    def __init__(self, embedder, vector_db, llm):
        self.embedder = embedder
        self.vector_db = vector_db
        self.llm = llm

    def query(self, question):
        try:
            embedding = self.embedder.embed(question)
            results = self.vector_db.search(embedding)

            context = "\n\n".join([m["metadata"]["text"] for m in results])

            prompt = f"""
You are a fraud analytics assistant. You will answer the question based on the provided context. Do not make up answers. If the context does not contain the answer, say "I don't know".

Context:
{context}

Question: {question}

Provide a clear answer with reasoning.
"""
            return self.llm.ask(prompt)
        except Exception as e:
            raise Exception(f"RAG Pipeline Failed: {e}")
