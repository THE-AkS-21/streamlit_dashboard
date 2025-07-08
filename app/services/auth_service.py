# app/services/auth_service.py
import hashlib
from typing import Optional

class AuthService:
    def __init__(self):
        # In production, this should be in a database
        self.users = {
            "admin": hashlib.sha256("admin123".encode()).hexdigest(),
            "user": hashlib.sha256("user123".encode()).hexdigest()
        }

    def verify_credentials(self, username: str, password: str) -> bool:
        if username not in self.users:
            return False
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return self.users[username] == hashed_password