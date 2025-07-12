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
            transition: width 0.3s ease;
            overflow-x: hidden;
            z-index: 900;
            padding-top: 20px;
        }}
        .custom-sidebar:hover {{
            width: 220px;
        }}

        .sidebar-item {{
            display: flex;
            align-items: center;
            padding: 12px 16px;
            margin: 6px 12px;
            border-radius: 10px;
            color: #111827;
            font-weight: 500;
            text-decoration: none;
            transition: background-color 0.25s, transform 0.2s;
        }}

        .sidebar-item:hover {{
            background-color: #E0E7FF;
            transform: translateX(4px);
            border-left: 4px solid #2563EB;
        }}

        .sidebar-icon {{
            width: 28px;
            height: 28px;
            margin-right: 0px;
            flex-shrink: 0;
            transition: all 0.3s ease;
        }}

        .custom-sidebar:hover .sidebar-icon {{
            margin-right: 14px;
        }}

        .sidebar-label {{
            opacity: 0;
            transition: opacity 0.3s ease, margin 0.3s, color 0.3s;
            white-space: nowrap;
            font-size: 0.95rem;
            font-weight: 500;
            color: #374151;
            margin-left: 0;
            letter-spacing: 0.3px;
            padding-top: 2px;
        }}
        
        .custom-sidebar:hover .sidebar-label {{
            opacity: 1;
            margin-left: 6px;
            color: #1F2937;
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
            <a href="/?page=Dashboard" target="_self" class="sidebar-item">
                <img src="{load_icon('home.png')}" class="sidebar-icon">
                <div class="sidebar-label">Dashboard</div>
            </a>
            <a href="/?page=Analytics" target="_self" class="sidebar-item">
                <img src="{load_icon('analytics.png')}" class="sidebar-icon">
                <div class="sidebar-label">Analytics</div>
            </a>
            <a href="/?page=Settings" target="_self" class="sidebar-item">
                <img src="{load_icon('settings.png')}" class="sidebar-icon">
                <div class="sidebar-label">Settings</div>
            </a>
        </div>
    """, unsafe_allow_html=True)
