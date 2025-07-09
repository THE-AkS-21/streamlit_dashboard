import os
from typing import Optional, Dict, Tuple
from dataclasses import dataclass
import extra_streamlit_components as stx
from app.config.settings import AppConfig


@dataclass
class OAuthProvider:
    name: str
    client_id: str
    client_secret: str
    authorize_url: str
    token_url: str
    refresh_token_url: str
    userinfo_url: str
    scopes: list
    callback_url: str


class GoogleOAuthProvider:
    def __init__(self):
        self.config = AppConfig.google
        self.cookie_manager = stx.CookieManager()

    def get_provider(self) -> OAuthProvider:
        """Return Google OAuth provider configuration"""
        return OAuthProvider(
            name="google",
            client_id=self.config.client_id,
            client_secret=self.config.client_secret,
            authorize_url="https://accounts.google.com/o/oauth2/v2/auth",
            token_url="https://oauth2.googleapis.com/token",
            refresh_token_url="https://oauth2.googleapis.com/token",
            userinfo_url="https://www.googleapis.com/oauth2/v2/userinfo",
            scopes=[
                "openid",
                "https://www.googleapis.com/auth/userinfo.email",
                "https://www.googleapis.com/auth/userinfo.profile"
            ],
            callback_url=self.config.redirect_uri
        )

    def get_cookie_manager(self):
        """Return cookie manager instance"""
        return self.cookie_manager