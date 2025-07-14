# config.py

from dataclasses import dataclass, field
from typing import Optional
import os
import streamlit as st

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

def init_page_config():
    """
    Sets Streamlit page-level configuration and disables default Streamlit elements for production UI
    """
    logo_path = os.path.join("app/assets/icons/logo.png")
    st.set_page_config(
        page_title="BSC Dashboard",
        page_icon=logo_path,
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Hide Streamlit default menu, footer, hamburger etc.
    st.markdown("""
        <style>
        #MainMenu, header, footer, [data-testid="collapsedControl"] {
            display: none !important;
        }
        </style>
    """, unsafe_allow_html=True)

def hide_streamlit_default():
    # Disable Streamlit runtime rerun button and deploy banner for cleaner UI
    st.markdown("""
        <style>
        #MainMenu, footer, header {visibility: hidden;}
        [data-testid="stDeployButton"] {display: none !important;}
        [data-testid="stStatusWidget"] {display: none !important;}
        </style>
    """, unsafe_allow_html=True)
