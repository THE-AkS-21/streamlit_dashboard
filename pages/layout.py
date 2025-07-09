# app/views/layout.py
import streamlit as st
from app.utils.styles import load_css


class Layout:
    @staticmethod
    def render_navbar():
        with st.container():
            cols = st.columns([1, 6, 1])
            with cols[0]:
                st.image("app/assets/logo.png", width=50)
            with cols[1]:
                st.title("Analytics Dashboard")
            with cols[2]:
                if st.session_state.get("user_info"):
                    st.image(st.session_state.user_info.get("picture"), width=40)
                    if st.button("Logout"):
                        del st.session_state["user_info"]
                        st.experimental_rerun()

    @staticmethod
    def render_sidebar():
        st.markdown(load_css(), unsafe_allow_html=True)

        sidebar_html = """
        <div class="sidebar-hover">
            <div class="user-info">
                <img src="{}" style="width: 50px; border-radius: 50%;">
                <p>{}</p>
            </div>
            <div class="nav-item" onclick="handle_click('dashboard')">📊 Dashboard</div>
            <div class="nav-item" onclick="handle_click('analytics')">📈 Analytics</div>
            <div class="nav-item" onclick="handle_click('settings')">⚙️ Settings</div>
        </div>
        """.format(
            st.session_state.get("user_info", {}).get("picture", ""),
            st.session_state.get("user_info", {}).get("email", "")
        )

        st.markdown(sidebar_html, unsafe_allow_html=True)