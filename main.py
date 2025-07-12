import streamlit as st
from app.components.layout import render_layout
from app.pages import dashboard, analytics, settings
from app.constants import pages
from app.utils.global_styles import remove_all_top_spacing
from config import init_page_config, hide_streamlit_default

init_page_config()
remove_all_top_spacing()
hide_streamlit_default()

if __name__ == "__main__":
    render_layout()

current_page = st.session_state.get("current_page", pages.DASHBOARD)

if current_page == pages.DASHBOARD:
    dashboard.show_dashboard()
elif current_page == pages.ANALYTICS:
    analytics.show_analytics()
elif current_page == pages.SETTINGS:
    settings.show_settings()
