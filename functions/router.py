# class Router:
#     def __init__(self, llm):
#         self.llm = llm

#     def decide(self, question):
#         prompt = f"""
#                 You are a routing controller.
#                 Decide the MOST appropriate processing option for the question. Check for indication if the user is asking for an analysis with RAG, SQL, or just a general question.
#                 If the user mentions files, documents, or knowledge base, choose RAG.
#                 If the user mentions data, statistics, numbers, or analytics, choose SQL.
#                 If the user is asking a general question without specific context, choose GENERAL.

#                 Options:
#                 - GENERAL  → Use pure LLM reasoning, no DB and no RAG.
#                 - RAG      → Requires knowledge from uploaded documents / Pinecone.
#                 - SQL      → Requires numeric, statistical or fraud analytics from database.

#                 Return ONLY one word: GENERAL or RAG or SQL

#                 Question:
#                 {question}
#                 """
#         decision = self.llm.ask(prompt).strip().upper()

#         if "SQL" in decision:
#             return "SQL"
#         elif "RAG" in decision:
#             return "RAG"
#         else:
#             return "GENERAL"
