import streamlit as st

from app.components.content_area import render_sidebar_content_sync_script
from app.components.navbar import render_navbar
from app.components.sidebar import render_sidebar
from app.components.sidebar_toggle_script import render_sidebar_toggle_script
from app.utils.global_css import apply_global_styles


def render_layout():
    apply_global_styles()
    render_sidebar_toggle_script()
    render_sidebar_content_sync_script()

    query_params = st.query_params
    page = query_params.get("page", "Dashboard")

    # Open app container
    st.markdown("""<div id="app-container">""", unsafe_allow_html=True)
    render_navbar()
    render_sidebar(page)
