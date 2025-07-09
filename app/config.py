# app/config.py
from dataclasses import dataclass, field
from typing import Optional
import os

@dataclass
class DatabaseConfig:
    host: str = field(default_factory=lambda: os.getenv('DB_HOST', 'localhost'))
    port: int = field(default_factory=lambda: int(os.getenv('DB_PORT', '5432')))
    database: str = field(default_factory=lambda: os.getenv('DB_NAME', 'price_index_db'))
    user: str = field(default_factory=lambda: os.getenv('DB_USER', 'user'))
    password: str = field(default_factory=lambda: os.getenv('DB_PASSWORD', ''))

@dataclass
class AppConfig:
    debug: bool = field(default_factory=lambda: os.getenv('DEBUG', 'False').lower() == 'true')
    db: DatabaseConfig = field(default_factory=DatabaseConfig)