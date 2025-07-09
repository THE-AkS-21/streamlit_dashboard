import streamlit as st
from datetime import datetime, timedelta
import secrets
from app.config.settings import AppConfig


class SessionManager:
    @staticmethod
    def init_session():
        """Initialize session state"""
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        if 'user_info' not in st.session_state:
            st.session_state.user_info = None
        if 'auth_data' not in st.session_state:
            st.session_state.auth_data = None
        if 'auth_state' not in st.session_state:
            st.session_state.auth_state = None
        if 'last_activity' not in st.session_state:
            st.session_state.last_activity = None

    @staticmethod
    def generate_state(length: int = 32) -> str:
        """Generate secure state parameter"""
        return secrets.token_urlsafe(length)

    def set_user_session(self, user_info: dict, auth_data: dict):
        """Set user session data"""
        st.session_state.authenticated = True
        st.session_state.user_info = user_info
        st.session_state.auth_data = auth_data
        st.session_state.last_activity = datetime.now()

    def check_session_validity(self) -> bool:
        """Check if session is still valid"""
        if not st.session_state.get('authenticated', False):
            return False

        if st.session_state.get('last_activity'):
            expiry = st.session_state.last_activity + timedelta(
                seconds=AppConfig.session_expiry
            )
            if datetime.now() > expiry:
                self.clear_session()
                return False

        auth_data = st.session_state.get('auth_data', {})
        if not auth_data or 'access_token' not in auth_data:
            return False

        return True

    @staticmethod
    def clear_session():
        """Clear all session data"""
        keys_to_clear = [
            'authenticated',
            'user_info',
            'auth_data',
            'auth_state',
            'last_activity'
        ]
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]