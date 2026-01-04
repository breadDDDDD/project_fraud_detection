from google.genai import types
class RagPipeline:
    def __init__(self, embedder, vector_db, llm):
        self.embedder = embedder
        self.vector_db = vector_db
        self.llm = llm

    def query(self, question):
        try:
            embedding = self.embedder.embed(question)
            results = self.vector_db.search(embedding, top_k=5)

            context = "\n\n".join([m["metadata"]["text"] for m in results])

            prompt = f"""
You are a fraud analytics assistant. You will answer the question based on the provided context. Do not make up answers. If the context does not contain the answer, say "I don't know".

Context:
{context}

Question: {question}

Provide a clear answer with reasoning.

#FOLLOW THESE RULES
1. NEVER make up answers. If the information is not available, respond with "I don't have access to the required information".
2. FORMAT your responses in a user-friendly manner, providing explanations and reasoning when necessary.
3. DO NOT overthink your responses, keep them simple and to the point.
4. Keep any responses under 1000 words to reduce wait times.
"""
            return self.llm.worker(prompt)
        except Exception as e:
            raise Exception(f"RAG Pipeline Failed: {e}")
        
    def handle_tool_call(self, tool_call):
        if tool_call.name == "get_rag":
            return self.query(**tool_call.args)

        raise ValueError(f"Unknown tool: {tool_call.name}")
    
def get_rag_tool():
    return types.FunctionDeclaration(
        name="get_rag",
        description="Retrieve the answer from the provided context using RAG based on the question given.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "question": types.Schema(
                    type=types.Type.STRING,
                    description="the question asked by the user regarding the context provided."
                )
            },
            required=["question"]
        )
    )
