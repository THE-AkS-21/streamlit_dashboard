# app/database/connection.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import DatabaseConfig

def get_database_url(config: DatabaseConfig) -> str:
    return f"postgresql://{config.user}:{config.password}@{config.host}:{config.port}/{config.database}"

def create_db_engine(config: DatabaseConfig):
    return create_engine(get_database_url(config))

def get_session_maker(engine):
    return sessionmaker(bind=engine)