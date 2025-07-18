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

    # # ✅ Remove top space and align content correctly
    # st.markdown("""
    #     <style>
    #         /* Remove Streamlit's default top space */
    #         header, section.main > div:first-child {
    #             padding-top: 0 !important;
    #             margin-top: 0 !important;
    #         }
    #
    #         main.block-container {
    #             padding-top: 0 !important;
    #             margin-top: 0 !important;
    #         }
    #
    #         /* Remove top margin of first element (like h1) */
    #         .block-container h1:first-child {
    #             margin-top: 0 !important;
    #         }
    #
    #         /* Custom content offset exactly below navbar */
    #         .custom-content {
    #             margin-top: 0 !important;
    #             padding-top: 60px !important;  /* Height of navbar */
    #             transition: margin-left 0.3s ease;
    #         }
    #
    #         /* Sidebar collapse/expand sync */
    #         .custom-sidebar-collapsed ~ .custom-content {
    #             margin-left: 80px !important;
    #         }
    #
    #         .custom-sidebar-expanded ~ .custom-content {
    #             margin-left: 250px !important;
    #         }
    #     </style>
    # """, unsafe_allow_html=True)

