# config.py - Central configuration
from dataclasses import dataclass
from typing import Optional
import streamlit as st

@dataclass
class PageConfig:
    title: str = "Analytics Dashboard"
    icon: str = "📊"
    layout: str = "wide"
    initial_sidebar_state: str = "auto"


class AppConfig:
    # App-wide configuration settings
    DEBUG: bool = False
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None

    @classmethod
    def load_from_env(cls):
        # Load configuration from environment variables
        pass

def init_page_config():
    st.set_page_config(
        page_title="Custom Dashboard",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

def hide_streamlit_style():
    st.markdown("""
        <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            [data-testid="collapsedControl"] {display: none;}
        </style>
    """, unsafe_allow_html=True)