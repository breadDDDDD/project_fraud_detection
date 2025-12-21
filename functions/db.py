import pandas as pd
from sqlalchemy import create_engine, inspect
from utils.config import settings

class DatabaseService:
    def __init__(self):
        try:
            self.engine = create_engine(settings.DB_URL)
        except Exception as e:
            raise Exception(f"Database connection failed: {e}")

    def get_schema(self):
        try:
            inspector = inspect(self.engine)
            schema = {}

            for table in inspector.get_table_names():
                columns = inspector.get_columns(table)
                schema[table] = [
                    f"{col['name']} ({str(col['type'])})"
                    for col in columns
                ]

            return schema   
        except Exception as e:
            raise Exception(f"Schema fetch failed: {e}")
    
    def query(self, sql):
        try:
            return pd.read_sql(sql, self.engine)
        except Exception as e:
            raise Exception(f"SQL Query Failed: {e}")
