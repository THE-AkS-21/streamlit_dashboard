import streamlit as st
from app.components.navbar import render_navbar
from app.components.sidebar import render_sidebar

def render_layout():
    query_params = st.query_params  # ✅ modern replacement
    page = query_params.get("page", "Dashboard")  # note: no list wrapping now — single value or None

    render_navbar()
    render_sidebar(page)

    st.markdown("""
        <script>
        function initHamburger() {
            const hamburger = document.getElementById("hamburger-toggle");
            const sidebar = document.getElementById("custom-sidebar");
            if (hamburger && sidebar) {
                hamburger.onclick = function() {
                    sidebar.classList.toggle("show");
                }
            }
        }
        window.addEventListener("load", initHamburger);
        </script>
    """, unsafe_allow_html=True)
