from dotenv import load_dotenv
from sqlalchemy import create_engine

import os

load_dotenv()

DATABASE_URL = os.getenv("DB_URL")
engine = create_engine(DATABASE_URL)
