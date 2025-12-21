from google import genai
from utils.config import settings

class LLMService:
    def __init__(self):
        try:
            client = genai.Client(api_key= settings.GEMINI_API_KEY)
            self.client = client
        except Exception as e:
            raise Exception(f"Gemini init failed: {e}")

    def ask(self, prompt):
        try:
            response = self.client.models.generate_content(model = 'gemini-2.5-flash-lite',contents =prompt)
            return response.text
        except Exception as e:
            raise Exception(f"Gemini request failed: {e}")
