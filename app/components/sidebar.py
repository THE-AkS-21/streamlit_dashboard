import streamlit as st
from app.utils.icon_loader import load_icon

def render_sidebar():
    st.markdown("""
        <style>
        .custom-sidebar {
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
        }
        .custom-sidebar:hover {
            width: 220px;
        }
        .custom-sidebar.show {
            left: 0;
        }
        .sidebar-item {
            display: flex;
            align-items: center;
            padding: 16px;
            cursor: pointer;
            color: black;
        }
        .sidebar-item:hover {
            background-color: #F3F4F6;
        }
        .sidebar-icon {
            width: 22px;
            height: 22px;
            margin-right: 12px;
        }
        .sidebar-label {
            opacity: 0;
            transition: opacity 0.3s;
        }
        .custom-sidebar:hover .sidebar-label {
            opacity: 1;
        }
        @media screen and (max-width: 768px) {
            .custom-sidebar {
                left: -220px;
                width: 220px;
            }
            .custom-sidebar.show {
                left: 0;
            }
        }
        </style>
        <div class="custom-sidebar">
    """, unsafe_allow_html=True)

    pages = {
        "Dashboard": "home.svg",
        "Analytics": "analytics.png",
        "Settings": "settings.png"
    }

    for page, icon_file in pages.items():
        icon = load_icon(icon_file)
        if st.button(f" {page}", key=page):
            st.session_state["current_page"] = page

        st.markdown(f"""
            <div class="sidebar-item">
                <img src="{icon}" class="sidebar-icon">
                <div class="sidebar-label">{page}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
