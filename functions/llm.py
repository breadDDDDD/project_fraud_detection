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
            response = self.client.models.generate_content(model = settings.GEMINI_MODEL ,contents =prompt)
            return response.text
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            if hasattr(e, "response"):
                print(e.response)
            raise Exception(f"Gemini request failed: {e}")
