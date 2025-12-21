import streamlit as st
from functions.db import DatabaseService
from functions.embedding import EmbeddingService
from functions.vector_service import VectorService
from functions.llm import LLMService
from functions.rag import RagPipeline
from functions.sql import SQLPipeline
from functions.add_document import DocumentIngestor
from functions.router import Router

st.set_page_config(page_title="Fraud AI Chatbot", layout="wide")

st.title("Fraud Chatbot")

@st.cache_resource
def load_services():
    db = DatabaseService()
    embedder = EmbeddingService()
    vector = VectorService()
    llm = LLMService()

    rag = RagPipeline(embedder, vector, llm)
    sql = SQLPipeline(db, llm)
    doc = DocumentIngestor(embedder, vector)
    router = Router(llm)

    return llm, rag, sql, doc, router

llm, rag_pipeline, sql_pipeline, doc_ingestor, router = load_services()
col1, col2 = st.columns([4, 2])

with col1:
    question = st.text_input("Ask your question")

# with col2:
#     mode = st.radio(
#         "Mode",
#         ["General Chat", "RAG Mode", "SQL Analytics"],
#         horizontal=True
#     )

# if st.button("Send") and question:
#     with st.spinner("Thinking..."):
#         try:
#             if mode == "General Chat":
#                 answer = llm.ask(question)

#             elif mode == "RAG Mode":
#                 answer = rag_pipeline.query(question)

#             elif mode == "SQL Analytics":
#                 answer = sql_pipeline.run(question)

#             st.success(answer)

#         except Exception as e:
#             st.error(str(e))
if st.button("Send") and question:
    with st.spinner("Thinking..."):
        try:
            mode = router.decide(question)

            if mode == "GENERAL":
                answer = llm.ask(question)

            elif mode == "RAG":
                answer = rag_pipeline.query(question)

            elif mode == "SQL":
                answer = sql_pipeline.run(question)

            # st.info(f"mmode Selected: {mode}")
            st.success(answer)

        except Exception as e:
            st.error(str(e))

st.subheader("Upload Knowledge File")

uploaded_file = st.file_uploader(
    "Upload PDF / TXT / CSV",
    type=["pdf", "txt", "csv"]
)

if uploaded_file and st.button("add Document"):
    with st.spinner("Processing & embedding"):
        try:
            msg = doc_ingestor.ingest(uploaded_file)
            st.success(msg)
        except Exception as e:
            st.error(str(e))