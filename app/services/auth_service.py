import streamlit as st
from typing import Tuple, Optional
import requests
from app.auth.oauth_provider import GoogleOAuthProvider
from app.utils.session import SessionManager


class AuthService:
    def __init__(self):
        self.provider = GoogleOAuthProvider()
        self.session_manager = SessionManager()

    def initialize_login(self) -> Tuple[str, str]:
        """Initialize OAuth login"""
        try:
            provider_config = self.provider.get_provider()

            # Generate state
            state = SessionManager.generate_state()
            st.session_state.auth_state = state

            # Build authorization URL
            params = {
                'client_id': provider_config.client_id,
                'redirect_uri': provider_config.callback_url,
                'scope': ' '.join(provider_config.scopes),
                'state': state,
                'response_type': 'code',
                'access_type': 'offline',
                'prompt': 'consent'
            }

            # Build authorization URL
            authorize_url = f"{provider_config.authorize_url}?"
            authorize_url += "&".join(f"{key}={requests.utils.quote(str(value))}"
                                      for key, value in params.items())

            return authorize_url, state

        except Exception as e:
            raise Exception(f"Failed to initialize login: {str(e)}")

    def handle_callback(self, state: str, code: str) -> Optional[dict]:
        """Handle OAuth callback"""
        try:
            provider_config = self.provider.get_provider()

            # Exchange code for token
            token_response = requests.post(
                provider_config.token_url,
                data={
                    'client_id': provider_config.client_id,
                    'client_secret': provider_config.client_secret,
                    'code': code,
                    'grant_type': 'authorization_code',
                    'redirect_uri': provider_config.callback_url
                }
            )

            if token_response.status_code != 200:
                raise Exception("Failed to get access token")

            token_data = token_response.json()

            # Get user info
            userinfo_response = requests.get(
                provider_config.userinfo_url,
                headers={'Authorization': f'Bearer {token_data["access_token"]}'}
            )

            if userinfo_response.status_code != 200:
                raise Exception("Failed to get user info")

            user_info = userinfo_response.json()

            # Store tokens and user info in session
            self.session_manager.set_user_session(
                user_info=user_info,
                auth_data={
                    'access_token': token_data.get('access_token'),
                    'refresh_token': token_data.get('refresh_token'),
                    'expires_in': token_data.get('expires_in')
                }
            )

            return user_info

        except Exception as e:
            raise Exception(f"Authentication failed: {str(e)}")

    def refresh_token(self) -> bool:
        """Refresh access token"""
        try:
            provider_config = self.provider.get_provider()
            auth_data = st.session_state.get('auth_data', {})
            refresh_token = auth_data.get('refresh_token')

            if not refresh_token:
                return False

            response = requests.post(
                provider_config.refresh_token_url,
                data={
                    'client_id': provider_config.client_id,
                    'client_secret': provider_config.client_secret,
                    'refresh_token': refresh_token,
                    'grant_type': 'refresh_token'
                }
            )

            if response.status_code != 200:
                return False

            token_data = response.json()
            auth_data.update({
                'access_token': token_data['access_token'],
                'expires_in': token_data['expires_in']
            })

            st.session_state.auth_data = auth_data
            return True

        except Exception:
            return False

    def logout(self):
        """Clear user session"""
        self.session_manager.clear_session()