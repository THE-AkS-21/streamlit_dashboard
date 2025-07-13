import streamlit as st

from app.components.toolbar import render_toolbar
from app.utils.icon_loader import load_icon

@st.cache_resource(show_spinner=False)
def render_sidebar(page):
    """Render responsive sidebar with mobile toolbar integration"""
    actions = render_toolbar(page)  # fetch dropdown actions for current page

    st.markdown(f"""
        <style>
        :root {{
            --accent: #00AEEF;
            --sidebar-bg: #F3F4F6;
            --hover-bg: #D1D5DB;
            --text-main: #111827;
        }}
        .custom-sidebar {{
            position: fixed;
            top: 60px; /* ← 30px navbar + 30px toolbar */
            left: 0;
            height: calc(100% - 60px);
            width: 50px;
            background-color: var(--sidebar-bg);
            transition: width 0.3s ease, left 0.3s ease;
            overflow-x: hidden;
            z-index: 900;
            padding-top: 3px;
        }}
        .custom-sidebar a {{
            text-decoration: none !important;
            color: inherit;
        }}
        .custom-sidebar:hover {{
            width: 180px;
        }}
        .sidebar-item {{
            display: flex;
            align-items: center;
            padding: 5px 2px;
            margin: 6px 12px;
            border-radius: 10px;
            color: var(--text-main);
            font-weight: 500;
            transition: background-color 0.25s, transform 0.2s;
        }}
        .sidebar-item:hover {{
            background-color: var(--hover-bg);
            transform: translateX(4px);
            border-left: 4px solid var(--accent);
        }}
        .sidebar-icon {{
            width: 28px;
            height: 28px;
            flex: 0 0 auto;
            min-width: 28px;
            max-width: 28px;
            min-height: 28px;
            max-height: 28px;
            transition: all 0.3s ease;
            margin-right: 0;
        }}
        .sidebar-label {{
            display: inline-block;
            overflow: hidden;
            white-space: nowrap;
            font-size: 0.95rem;
            font-weight: 500;
            color: #60A5FA;
            margin-left: 12px;
            opacity: 0;
            transition: opacity 0.3s ease, color 0.3s ease;
        }}
        .custom-sidebar:hover .sidebar-label {{
            opacity: 1;
        }}
        .sidebar-item:hover .sidebar-label {{
            color: #00AEEF;
        }}
        .custom-content {{
            margin-top: 60px;
            margin-left: 70px;
            padding: 20px;
            transition: margin-left 0.3s ease;
        }}
        .custom-sidebar:hover ~ .custom-content {{
            margin-left: 180px;
        }}
        .sidebar-item.current-page {{
            background-color: var(--hover-bg);
            border-left: 4px solid var(--accent);
            color: var(--text-main);
            font-weight: 600;
        }}
        .sidebar-item.current-page .sidebar-label {{
            color: var(--accent);
        }}
        @media screen and (max-width: 768px) {{
            .custom-sidebar {{
                top: 30px;
                left: 0;
                width: 180px;
            }}
            .custom-sidebar.show {{
                left: 0;
            }}
            .custom-content {{
                margin-left: 0;
            }}
            .custom-sidebar .sidebar-label {{
                opacity: 1;
            }}

        }}
        </style>

        <div class="custom-sidebar" id="custom-sidebar">
            <a href="/?page=Dashboard" target="_self" class="sidebar-item {'current-page' if page == 'Dashboard' else ''}">
                <img src="{load_icon('home.png')}" class="sidebar-icon">
                <span class="sidebar-label">Home</span>
            </a>
            <a href="/?page=Analytics" target="_self" class="sidebar-item {'current-page' if page == 'Analytics' else ''}">
                <img src="{load_icon('analytics.png')}" class="sidebar-icon">
                <span class="sidebar-label">Analytics</span>
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
        @media screen and (min-width: 768px) {{
            #mobile-toolbar-items {{
                display: none;
            }}
        }}
        </style>
    """, unsafe_allow_html=True)
