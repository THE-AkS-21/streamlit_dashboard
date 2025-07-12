import streamlit as st
from app.components.layout import render_layout
from app.pages import dashboard, analytics, settings
from app.constants import pages
from config import init_page_config, hide_streamlit_default

init_page_config()
hide_streamlit_default()
render_layout()

current_page = st.session_state.get("current_page", pages.DASHBOARD)

if current_page == pages.DASHBOARD:
    dashboard.show_dashboard()
elif current_page == pages.ANALYTICS:
    analytics.show_analytics()
elif current_page == pages.SETTINGS:
    settings.show_settings()

st.markdown('</div>', unsafe_allow_html=True)
