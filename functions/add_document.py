import uuid
import os
import pandas as pd

class DocumentIngestor:
    def __init__(self, embedder, vector_db):
        self.embedder = embedder
        self.vector_db = vector_db

    def load_file(self, file):
        ext = os.path.splitext(file.name)[1].lower()

        if ext in [".txt"]:
            return file.read().decode("utf-8")

        elif ext in [".pdf"]:
            import PyPDF2
            reader = PyPDF2.PdfReader(file)
            return "\n".join([page.extract_text() for page in reader.pages])

        elif ext in [".csv"]:
            df = pd.read_csv(file)
            return df.to_string()

        else:
            raise Exception("Unsupported file type")

    def chunk_text(self, text, chunk_size=500):
        words = text.split()
        chunks = []

        for i in range(0, len(words), chunk_size):
            chunk = " ".join(words[i:i + chunk_size])
            chunks.append(chunk)

        return chunks

    def ingest(self, file):
        try:
            raw_text = self.load_file(file)
            chunks = self.chunk_text(raw_text)

            for chunk in chunks:
                embedding = self.embedder.embed(chunk)

                self.vector_db.upsert(
                    id=str(uuid.uuid4()),
                    embedding=embedding,
                    metadata={"text": chunk}
                )

            return f"Uploaded {len(chunks)} chunks successfully 🎉"

        except Exception as e:
            raise Exception(f"Document ingestion failed: {e}")
