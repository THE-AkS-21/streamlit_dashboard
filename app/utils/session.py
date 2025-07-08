# app/utils/session.py
import streamlit as st
from typing import Optional

def init_session_state():
    """Initialize session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'username' not in st.session_state:
        st.session_state.username = None

def get_authenticated_user() -> Optional[str]:
    """Get currently authenticated username"""
    return st.session_state.username if st.session_state.authenticated else None

def set_authenticated_user(username: str):
    """Set authenticated user"""
    st.session_state.authenticated = True
    st.session_state.username = username

def clear_authenticated_user():
    """Clear authentication"""
    st.session_state.authenticated = False
    st.session_state.username = None