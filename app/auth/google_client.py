from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from app.config.settings import AppConfig


class GoogleOAuthClient:
    def __init__(self):
        self.config = AppConfig.google

    def create_auth_flow(self) -> Flow:
        """Create OAuth 2.0 flow instance"""
        return Flow.from_client_config(
            {
                "web": {
                    "client_id": self.config.client_id,
                    "client_secret": self.config.client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                }
            },
            scopes=self.config.scope,
            redirect_uri=self.config.redirect_uri
        )

    def get_user_info(self, credentials: Credentials) -> dict:
        """Fetch user information from Google"""
        try:
            service = build('oauth2', 'v2', credentials=credentials)
            user_info = service.userinfo().get().execute()
            return user_info
        except Exception as e:
            raise Exception(f"Failed to fetch user info: {str(e)}")