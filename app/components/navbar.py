import streamlit as st
from app.utils.icon_loader import load_icon

@st.cache_resource(show_spinner=False)
def render_navbar():
    if "sidebar_open" not in st.session_state:
        st.session_state.sidebar_open = False

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
            justify-content: space-between;
            padding: 0 14px;
            z-index: 1000;
        }}
        .navbar-logo {{
            width: 22px;
            height: 22px;
        }}
        .navbar-title {{
            font-size: 0.85rem;
            font-weight: 600;
            color: #00AEEF;
            margin: 0;
            padding: 0;
            line-height: 1;
        }}
        .hamburger {{
            width: 24px;
            height: 24px;
            cursor: pointer;
            display: none;
        }}
        .navbar-left {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        @media screen and (max-width: 768px) {{
            .hamburger {{
                display: block;
            }}
            .navbar-left {{
                display: none;
            }}
            .navbar-title {{
                flex: 1;
                text-align: center;
            }}
        }}
        </style>

        <div class="custom-navbar">
            <img src="{load_icon('menu.png')}" class="hamburger" onclick="window.parent.postMessage({{toggleSidebar: true}}, '*')">
            <div class="navbar-left" style="display:flex; align-items:center; gap:10px;">
                <img src="{load_icon('logo.png')}" class="navbar-logo">
                <p class="navbar-title">Bombay Shaving Company</p>
            </div>
        </div>

        <script>
        window.addEventListener("message", (event) => {{
            if (event.data.toggleSidebar) {{
                const sidebar = document.querySelector('.custom-sidebar');
                sidebar.classList.toggle('show');
            }}
        }});
        </script>
    """, unsafe_allow_html=True)
