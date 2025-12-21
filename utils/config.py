import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DB_URL = os.getenv("DB_URL")

    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_INDEX = os.getenv("PINECONE_INDEX")

    OLLAMA_HOST = os.getenv("OLLAMA_HOST")
    OLLAMA_EMBED_MODEL = os.getenv("OLLAMA_EMBED_MODEL")

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL")

settings = Settings()
