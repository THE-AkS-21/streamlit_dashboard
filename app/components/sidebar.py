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
                <img src="{load_icon('dashboard.svg')}" class="sidebar-icon">
                <span class="sidebar-label">Dashboard</span>
            </a>
            <a href="/?page=Analytics" target="_self" class="sidebar-item {'current-page' if page == 'Analytics' else ''}">
                <img src="{load_icon('analytics.svg')}" class="sidebar-icon">
                <span class="sidebar-label">Analytics</span>
            </a>
            <a href="/?page=Upload" target="_self" class="sidebar-item {'current-page' if page == 'Upload' else ''}">
                <img src="{load_icon('import.svg')}" class="sidebar-icon">
                <span class="sidebar-label">Import</span>
            </a>
            <a href="/?page=Settings" target="_self" class="sidebar-item {'current-page' if page == 'Settings' else ''}">
                <img src="{load_icon('profile.svg')}" class="sidebar-icon">
                <span class="sidebar-label">Profile</span>
            </a>
            <div class="sidebar-footer" id="mobile-toolbar-items">
                {"".join(f'<a href="{url}" class="sidebar-item"><span class="sidebar-label">{label}</span></a>' for label, url in actions)}
            </div>
            <a href="/?page=Logout" target="_self" class="sidebar-item">
                <img src="{load_icon('logout.svg')}" class="sidebar-icon">
                <span class="sidebar-label">Logout</span>
            </a>
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

