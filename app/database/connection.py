from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import pandas as pd
import streamlit as st

# Cache the engine instance
@st.cache_resource(show_spinner="Connecting to database...")
def get_engine():
    return create_engine(
        f"postgresql://{st.secrets.postgres.user}:{st.secrets.postgres.password}@"
        f"{st.secrets.postgres.host}:{st.secrets.postgres.port}/{st.secrets.postgres.dbname}"
    )

class DatabaseConnection:
    def __init__(self):
        self.engine = get_engine()
        self.Session = sessionmaker(bind=self.engine)

    @contextmanager
    def get_connection(self):
        conn = self.engine.connect()
        try:
            yield conn
        finally:
            conn.close()

    def execute_query(self, query: str, params: dict = None) -> pd.DataFrame:
        with self.get_connection() as conn:
            return run_cached_query(conn, query, params)

    def execute_write_query(self, query: str, params: dict = None) -> None:
        with self.Session() as session:
            session.execute(text(query), params or {})
            session.commit()

@st.cache_data(ttl=3600)
def run_cached_query(_conn, query: str, params: dict = None) -> pd.DataFrame:
    params = params or {}
    return pd.read_sql_query(text(query), _conn, params=params)

# Single instance
db = DatabaseConnection()
