from dataclasses import dataclass
from typing import Optional
import streamlit as st
import os

@dataclass
class PageConfig:
    title: str = "Analytics Dashboard"
    icon: str = "📊"
    layout: str = "wide"
    initial_sidebar_state: str = "auto"

class AppConfig:
    DEBUG: bool = False
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None

def init_page_config():
    logo_path = os.path.join("app/assets/icons/logo.png")  # adjust if needed
    st.set_page_config(
        page_title="BSC Dashboard",
        page_icon=logo_path,
        layout="wide",
        initial_sidebar_state="collapsed"
    )

def hide_streamlit_default():
    st.markdown("""
        <style>
        #MainMenu, footer, header {visibility: hidden;}
        [data-testid="collapsedControl"] {display: none;}
        </style>
    """, unsafe_allow_html=True)
