import streamlit as st
from app.utils.icon_loader import load_icon

def render_navbar():
    st.markdown(f"""
        <style>
        .custom-navbar {{
            position: fixed;
            top: 0;
            left: 0;
            height: 50px;
            width: 100%;
            background-color: #E5E7EB;
            display: flex;
            align-items: center;
            padding: 0 14px;
            
        }}
        .navbar-logo {{
            width: 26px;
            height: 26px;
            margin-right: 8px;
        }}
        .navbar-title {{
            font-size: 0.5rem;
            font-weight: 500;
            color: #00AEEF;
            margin: 0;
            padding: 0;
            flex: 1;
            line-height: 1;
            white-space: nowrap;
        }}
        .hamburger {{
            font-size: 22px;
            cursor: pointer;
            display: none;
        }}
        @media screen and (max-width: 768px) {{
            .hamburger {{
                display: block;
            }}
        }}
        </style>

        <div class="custom-navbar">
            <img src="{load_icon('logo.png')}" class="navbar-logo">
            <p class="navbar-title">Bombay Shaving Company</p>
            <div class="hamburger" onclick="document.querySelector('.custom-sidebar').classList.toggle('show')">☰</div>
        </div>
    """, unsafe_allow_html=True)
