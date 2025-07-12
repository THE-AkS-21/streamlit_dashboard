
from sqlalchemy import create_engine, text
from contextlib import contextmanager
import pandas as pd
import streamlit as st

@st.cache_resource(show_spinner="Connecting to Database...")
def get_engine():
    return create_engine(
        f"postgresql://{st.secrets.postgres.user}:{st.secrets.postgres.password}@"
        f"{st.secrets.postgres.host}:{st.secrets.postgres.port}/{st.secrets.postgres.dbname}"
    )

class DatabaseConnection:
    def __init__(self):
        self.engine = get_engine()

    @contextmanager
    def get_connection(self):
        conn = self.engine.connect()
        try:
            yield conn
        finally:
            conn.close()
            self.engine.dispose()
    @st.cache_data(ttl=3600, show_spinner=False, allow_output_mutation=True, hash_funcs={pd.DataFrame: lambda _: None})
    def execute_query(self, query: str, params: dict = None) -> pd.DataFrame:
        with self.get_connection() as conn:
            return pd.read_sql_query(text(query), conn, params=params)

    def execute_write_query(self, query: str, params: dict = None) -> None:
        with self.get_connection() as conn:
            conn.execute(text(query), params or {})
            conn.commit()

db = DatabaseConnection()