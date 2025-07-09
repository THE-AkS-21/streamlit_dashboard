import os
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()

@dataclass
class GoogleAuthConfig:
    client_id: str = os.getenv('GOOGLE_CLIENT_ID', '')
    client_secret: str = os.getenv('GOOGLE_CLIENT_SECRET', '')
    redirect_uri: str = os.getenv('REDIRECT_URI', 'http://localhost:8501/callback')
    scope: list = ('openid', 'https://www.googleapis.com/auth/userinfo.email',
                  'https://www.googleapis.com/auth/userinfo.profile')

@dataclass
class AppConfig:
    debug: bool = os.getenv('DEBUG', 'False').lower() == 'true'
    session_expiry: int = int(os.getenv('SESSION_EXPIRY', '3600'))
    google = GoogleAuthConfig()