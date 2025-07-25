import streamlit as st
from app.components.toolbar import render_toolbar
from app.utils.icon_loader import load_icon

# @st.cache_resource(show_spinner=False)
def render_sidebar(page):
    """Render responsive sidebar with mobile toolbar integration"""
    actions = render_toolbar(page)  # fetch dropdown actions for current page

    st.markdown(f"""
        <div class="custom-sidebar" id="custom-sidebar">
            <a href="/?page=Dashboard" target="_self" class="sidebar-item {'current-page' if page == 'Dashboard' else ''}">
                <img src="{load_icon('home.png')}" class="sidebar-icon">
                <span class="sidebar-label">Home</span>
            </a>
            <a href="/?page=Analytics" target="_self" class="sidebar-item {'current-page' if page == 'Analytics' else ''}">
                <img src="{load_icon('analytics.png')}" class="sidebar-icon">
                <span class="sidebar-label">PNL Analytics</span>
            </a>
            <a href="/?page=sku_analytics" target="_self" class="sidebar-item {'current-page' if page == 'sku_analytics' else ''}">
                <img src="{load_icon('box.png')}" class="sidebar-icon">
                <span class="sidebar-label">SKU Analytics</span>
            </a>
            <a href="/?page=Settings" target="_self" class="sidebar-item {'current-page' if page == 'Settings' else ''}">
                <img src="{load_icon('settings.png')}" class="sidebar-icon">
                <span class="sidebar-label">Settings</span>
            </a>
            <div class="sidebar-footer" id="mobile-toolbar-items">
                {"".join(f'<a href="{url}" class="sidebar-item"><span class="sidebar-label">{label}</span></a>' for label, url in actions)}
            </div>
        </div>
        <style>
        /* Remove padding and margin from Streamlit's native sidebar container */
            section[data-testid="stSidebar"] > div:first-child {{
                padding: 0;
                margin: 0;
            }}
        @media screen and (min-width: 768px) {{
            #mobile-toolbar-items {{
                display: none;
            }}
        }}
        </style>
    """, unsafe_allow_html=True)

