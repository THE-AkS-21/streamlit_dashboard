import streamlit as st
from app.utils.icon_loader import load_icon

@st.cache_resource(show_spinner=False)
def render_sidebar():
    st.markdown(f"""
        <style>
        .custom-sidebar {{
            position: fixed;
            top: 50px;
            left: 0;
            height: calc(100% - 50px);
            width: 50px;
            background-color: #E5E7EB;
            transition: width 0.3s ease;
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
            color: #111827;
            font-weight: 500;
            transition: background-color 0.25s, transform 0.2s;
        }}

        .sidebar-item:hover {{
            background-color: #E0E7FF;
            transform: translateX(4px);
            border-left: 4px solid #00AEEF;
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
            margin-top: 50px;
            margin-left: 70px;
            padding: 20px;
            transition: margin-left 0.3s ease;
        }}

        .custom-sidebar:hover ~ .custom-content {{
            margin-left: 220px;
        }}

        @media screen and (max-width: 768px) {{
            .custom-sidebar {{
                left: -220px;
                width: 220px;
            }}
            .custom-sidebar.show {{
                left: 0;
            }}
            .custom-content {{
                margin-left: 0;
            }}
        }}
        </style>

        <div class="custom-sidebar">
            <a href="/?page=Dashboard" target="_self" class="sidebar-item">
                <img src="{load_icon('home.png')}" class="sidebar-icon">
                <span class="sidebar-label">Home</span>
            </a>
            <a href="/?page=Analytics" target="_self" class="sidebar-item">
                <img src="{load_icon('analytics.png')}" class="sidebar-icon">
                <span class="sidebar-label">Analytics</span>
            </a>
            <a href="/?page=Settings" target="_self" class="sidebar-item">
                <img src="{load_icon('settings.png')}" class="sidebar-icon">
                <span class="sidebar-label">Settings</span>
            </a>
        </div>
    """, unsafe_allow_html=True)
