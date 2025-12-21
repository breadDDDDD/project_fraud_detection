from pinecone import Pinecone, ServerlessSpec
from utils.config import settings

class VectorService:
    def __init__(self):
        try:
            self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
            self.index = self.pc.Index(settings.PINECONE_INDEX)
        except Exception as e:
            raise Exception(f"Pinecone Init Failed: {e}")

    def upsert(self, id, embedding, metadata):
        try:
            self.index.upsert(vectors=[{"id": id, "values": embedding, "metadata": metadata}])
        except Exception as e:
            raise Exception(f"Pinecone Upsert Failed: {e}")

    def search(self, embedding, top_k=5):
        try:
            result = self.index.query(vector=embedding, top_k=top_k, include_metadata=True)
            return result["matches"]
        except Exception as e:
            raise Exception(f"Pinecone Search Failed: {e}")
