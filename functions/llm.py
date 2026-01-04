from google import genai
from google.genai import types
from utils.config import settings
import traceback
# from function_call.rag_toolcall import get_rag
# from function_call.sql_toolcall import get_sql
from functions.rag import get_rag_tool
from functions.sql import get_sql_tool

class LLMService:
    def __init__(self, sql_pipeline=None, rag_pipeline=None):
        try:
            client = genai.Client(api_key= settings.GEMINI_API_KEY)
            tools = types.Tool(function_declarations=[get_rag_tool(), get_sql_tool()])
            router_config=types.GenerateContentConfig(tools=[tools],
                                               tool_config=types.ToolConfig(function_calling_config=types.FunctionCallingConfig(mode='AUTO')))
            worker_config=types.GenerateContentConfig()
            self.client = client
            self.router_config = router_config
            self.worker_config = worker_config
            self.sql_pipeline = sql_pipeline
            self.rag_pipeline = rag_pipeline
        except Exception as e:  
            raise Exception(f"Gemini init failed: {e}")
        
    def _handle_tool_call(self, tool_call):
        name = tool_call.name
        if name == "get_sql":
            return self.sql_pipeline.handle_tool_call(tool_call)
        if name == "get_rag":
            return self.rag_pipeline.handle_tool_call(tool_call)

        raise ValueError(f"Unknown tool called: {name}")

    def main_system_prompt(self, question):
        return(f"""
    #MAIN INSTRUCTIONS
    You are a Fraud Detecttion AI Assistant. You will answer the user's question based on information gathered from RAG or SQL. Here are the instructions you WILL FOLLOW:
    1. ONLY use tool calls when necessary, when the user's question REQUIRES information from the database or external context.
    2. the ONLY tool call available to you are 'get_sql' and 'get_rag'.
    3. When using 'get_sql', you MUST generate an SQL query based on the user's question and the database schema to retrieve relevant information.
    4. When using 'get_rag', you MUST retrieve information from the provided context to answer the user's question.
    5. ALWAYS provide clear and concise answers based on the information retrieved.
    
    #TOOL CALLING INSTRUCTIONS
    1. When the user asks a question that requires information from a database, use the 'get_sql' tool call.
    2. When the user asks a question that requires information from external context/document, use the 'get_rag' tool call.
    3. ALWAYS provide the 'question' parameter in your tool calls, which is the user's original question.
    4. Be concise, clear, and specific when creating a summary from the tool call output, DO NOT add unnecessary information.
    5. If the tool call returns no relevant information, respond with "No relevant Information available". 
      
    #SAFETY INSTRUCTIONS
    1. ALWAYS prioritize user safety and data privacy.
    2. DO NOT say any explicit words or harmful content unless originating from the information retrieved.
    3. When creating a SQL Query, AVOID accessing sensitive information unless explicitly asked by the user and ensure compliance with data privacy regulations.
    
    ##USER QUESTION
    User Question: {question}
    """)
        
    
    def worker(self, prompt):
        return self.client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt, config=self.worker_config
        ).text
    
    def ask(self, prompt):
        try:
            final_prompt = self.main_system_prompt(prompt)
            response = self.client.models.generate_content(model = settings.GEMINI_MODEL ,contents =final_prompt, config=self.router_config)
            for part in response.candidates[0].content.parts:
                if part.function_call:
                    return self._handle_tool_call(part.function_call)
            return response.text
        except Exception as e:
            print(traceback.format_exc())
            if hasattr(e, "response"):
                print(e.response)
            raise Exception(f"Gemini request failed: {e}")


