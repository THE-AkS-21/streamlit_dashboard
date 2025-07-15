from dataclasses import dataclass, field
import os
import streamlit as st

# Database configuration loaded from environment variables (safe — no hardcoded secrets)
@dataclass
class DatabaseConfig:
    host: str = field(default_factory=lambda: os.getenv('DB_HOST', 'localhost'))
    port: int = field(default_factory=lambda: int(os.getenv('DB_PORT', '5432')))
    database: str = field(default_factory=lambda: os.getenv('DB_NAME', 'price_index_db'))
    user: str = field(default_factory=lambda: os.getenv('DB_USER', 'user'))
    password: str = field(default_factory=lambda: os.getenv('DB_PASSWORD', ''))

# App-wide configurations
@dataclass
class AppConfig:
    debug: bool = field(default_factory=lambda: os.getenv('DEBUG', 'False').lower() == 'true')
    cache_ttl: int = 3600  # 1 hour cache expiry
    animation_speed: float = 0.25  # CSS transitions in seconds
    db: DatabaseConfig = field(default_factory=DatabaseConfig)

# Global app config instance
config = AppConfig()

def init_page_config():
    """Set Streamlit page-level config and disable default Streamlit UI elements"""
    logo_path = os.path.join("app/assets/icons/logo.png")
    st.set_page_config(
        page_title="BSC Dashboard",
        page_icon=logo_path,
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    # Hide Streamlit menu, footer, deploy button etc.
    st.markdown("""
        <style>
        #MainMenu, header, footer, [data-testid="collapsedControl"],
        [data-testid="stDeployButton"], [data-testid="stStatusWidget"] {
            display: none !important;
        }
        </style>
    """, unsafe_allow_html=True)
