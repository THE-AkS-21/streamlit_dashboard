import streamlit as st
from app.components.layout import render_layout
from app.pages import dashboard, analytics, settings
from config import init_page_config, hide_streamlit_default

init_page_config()
hide_streamlit_default()
render_layout()

current_page = st.session_state.get("current_page", "Dashboard")

if current_page == "Dashboard":
    dashboard.show_dashboard()
elif current_page == "Analytics":
    analytics.show_analytics()
elif current_page == "Settings":
    settings.show_settings()

# Close the content wrapper div
st.markdown('</div>', unsafe_allow_html=True)
