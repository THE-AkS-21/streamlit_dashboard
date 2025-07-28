import streamlit as st
from app.components.navbar import render_navbar
from app.components.sidebar import render_sidebar
from app.components.sidebar_toggle_script import render_sidebar_toggle_script
from app.components.content_area import render_sidebar_content_sync_script
from app.utils.global_css import apply_global_styles

def render_layout():
    """Render the global styles, navbar, sidebar, and layout-related scripts"""
    apply_global_styles()

    # Sidebar collapse/expand toggle script and sidebar-content sync script
    render_sidebar_toggle_script()
    render_sidebar_content_sync_script()

    # Get current page param for sidebar active state
    query_params = st.query_params
    page = query_params.get("page", "Dashboard")

    # Render the navbar and sidebar
    render_navbar()
    render_sidebar(page)