import streamlit as st
from app.components.navbar import render_navbar
from app.components.sidebar import render_sidebar

def render_layout():
    render_navbar()
    render_sidebar()

    st.markdown("""
    <script>
    function initHamburger() {
        const hamburger = document.getElementById("hamburger-toggle");
        const sidebar = document.getElementById("sidebar");
        if (hamburger && sidebar) {
            hamburger.onclick = function() {
                sidebar.classList.toggle("show");
            }
        }
    }
    window.addEventListener("load", initHamburger);
    </script>
    """, unsafe_allow_html=True)
