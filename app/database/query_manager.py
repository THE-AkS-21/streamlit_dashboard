# app/database/query_manager.py
import pandas as pd
from sqlalchemy import create_engine, text
from app.config.settings import DATABASE_URL

class QueryManager:
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)

    def execute_query(self, query: str, params: dict = None) -> pd.DataFrame:
        """Execute SQL query and return results as pandas DataFrame"""
        try:
            with self.engine.connect() as connection:
                return pd.read_sql_query(text(query), connection, params=params)
        except Exception as e:
            print(f"Error executing query: {e}")
            return pd.DataFrame()

    def execute_raw_query(self, query: str, params: dict = None):
        """Execute SQL query and return raw results"""
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text(query), params)
                return result.fetchall()
        except Exception as e:
            print(f"Error executing query: {e}")
            return []