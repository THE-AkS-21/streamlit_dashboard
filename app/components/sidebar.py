import streamlit as st
from app.utils.icon_loader import load_icon

def render_sidebar():
    st.markdown(f"""
        <style>
        .custom-sidebar {{
            position: fixed;
            top: 60px;
            left: 0;
            height: calc(100% - 60px);
            width: 70px;
            background-color: #E5E7EB;
            border-right: 1px solid #D1D5DB;
            transition: width 0.3s;
            overflow-x: hidden;
            z-index: 900;
        }}
        .custom-sidebar:hover {{
            width: 220px;
        }}
        .sidebar-item {{
            display: flex;
            align-items: center;
            padding: 16px;
            cursor: pointer;
            color: black;
        }}
        .sidebar-item:hover {{
            background-color: #F3F4F6;
        }}
        .sidebar-icon {{
            width: 22px;
            height: 22px;
            margin-right: 12px;
        }}
        .sidebar-label {{
            opacity: 0;
            transition: opacity 0.3s;
            white-space: nowrap;
        }}
        .custom-sidebar:hover .sidebar-label {{
            opacity: 1;
        }}
        .custom-content {{
            margin-top: 60px;
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
            <a href="/?page=Dashboard" target="_self">
                <div class="sidebar-item">
                    <img src="{load_icon('home.svg')}" class="sidebar-icon">
                    <div class="sidebar-label">Dashboard</div>
                </div>
            </a>
            <a href="/?page=Analytics" target="_self">
                <div class="sidebar-item">
                    <img src="{load_icon('analytics.png')}" class="sidebar-icon">
                    <div class="sidebar-label">Analytics</div>
                </div>
            </a>
            <a href="/?page=Settings" target="_self">
                <div class="sidebar-item">
                    <img src="{load_icon('settings.png')}" class="sidebar-icon">
                    <div class="sidebar-label">Settings</div>
                </div>
            </a>
        </div>
    """, unsafe_allow_html=True)
