import requests
from utils.config import settings

class EmbeddingService:
    def __init__(self):
        self.base_url = settings.OLLAMA_HOST
        self.model = settings.OLLAMA_EMBED_MODEL

    def embed(self, text):
        try:
            res = requests.post(
                f"{self.base_url}/api/embeddings",
                json={"model": self.model, "prompt": text},
                timeout=20
            )
            res.raise_for_status()
            return res.json()["embedding"]
        except Exception as e:
            raise Exception(f"Embedding failed: {e}")
