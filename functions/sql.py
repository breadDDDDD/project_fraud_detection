import pandas as pd
import re
from google.genai import types

SQL_SYSTEM_PROMPT = """
You are an expert T-SQL generator.

Rules:
- Only generate valid Microsoft SQL Server queries
- Only use the database schema provided. NEVER invent tables or columns.
- SELECT only. NEVER UPDATE / DELETE / INSERT / DROP.
- Prefer aggregated insights when appropriate
- If the required table or column does not exist, pick the closest valid alternative from schema.
- DO NOT explain or use English. Output ONLY raw SQL.
- Output only the SQL. Do not say "Here is the query" or wrap it in ```sql``` blocks.
- Always limit results to maximum 100 rows using TOP or OFFSET/FETCH.
"""

SUMMARY_PROMPT = """
You are a fraud analytics expert.
1. Summarize the SQL result in clear, concise business language.
2. Explain patterns, trends and key takeaways.
3. NEVER make up answers. If the information is not available, respond with "I don't have access to the required information".
4. FORMAT your responses in a user-friendly manner, providing explanations and reasoning when necessary.
5. DO NOT overthink your responses, keep them simple and to the point.
6. Keep any responses under 1000 words to reduce wait times.
"""


class SQLPipeline:
    def __init__(self, db, llm):
        self.db = db
        self.llm = llm
    
    def clean_sql_output(self, query: str) -> str:
        query = re.sub(r"```sql|```|`", "", query, flags=re.IGNORECASE).strip()
        # Only keep text from the first SELECT to the first semicolon (if multiple statements)
        match = re.search(r"(select\b.*?;?)$", query, re.IGNORECASE | re.DOTALL)
        if match:
            query = match.group(1).strip()
        else:
            raise Exception("No valid SELECT statement found")
        return query

    def natural_to_sql(self, question, schema_info):
        prompt = f"""
                {SQL_SYSTEM_PROMPT}

                Question:
                {question}

                DATABASE SCHEMA:
                {schema_info}
                """

        sql_query = self.llm.worker(prompt).strip()
        sql_query = self.clean_sql_output(sql_query)
        return sql_query


    def enforce_sql_safety(self, query):
        q = query.lower()

        if "delete" in q or "drop" in q or "update" in q or "insert" in q:
            raise Exception("Blocked dangerous SQL command")

        if not q.startswith("select"):
            raise Exception("Only SELECT queries allowed")

        return query

    def execute_sql(self, query):
        try:
            query = self.enforce_sql_safety(query)
            df = self.db.query(query)

            if df is None or df.empty:
                return pd.DataFrame()
            return df

        except Exception as e:
            raise Exception(f"SQL execution failed: {e}")


    def summarize(self, df, question):
        try:
            prompt = f"""
            
{SUMMARY_PROMPT}

User Question:
{question}

Data:
{df.head(50).to_markdown()}

Provide insight:
"""
            return self.llm.worker(prompt)

        except Exception as e:
            raise Exception(f"Summary generation failed: {e}")


    def format_schema(self, schema):
        text = ""
        for table, cols in schema.items():
            text += f"TABLE: {table}\n"
            for c in cols:
                text += f"  - {c}\n"
            text += "\n"
        return text


    def run(self, question):
        try:
            schema = self.db.get_schema()
            schema_text = self.format_schema(schema)
            sql_query = self.natural_to_sql(question, schema_text)
            print("Generated SQL:", sql_query)
            df = self.execute_sql(sql_query)
            if df.empty:
                return "SQL executed successfully but returned no data available."
            summary = self.summarize(df, question)

            return f"""
                    {summary}
                    """
        except Exception as e:
            raise Exception(f"SQL Pipeline Failed: {e}")
        
    def handle_tool_call(self, tool_call):
        if tool_call.name == "get_sql":
            return self.run(**tool_call.args)

        raise ValueError(f"Unknown tool: {tool_call.name}")
        
def get_sql_tool():
    return types.FunctionDeclaration(
        name="get_sql",
        description="Generate an SQL query, retrieve the information, and generate a summary from the information based on the question given.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "question": types.Schema(
                    type=types.Type.STRING,
                    description="the question asked by the user regarding the information stored within the database."
                )
            },
            required=["question"]
        )
    )  
