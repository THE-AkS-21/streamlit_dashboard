import streamlit as st
from app.components.navbar import render_navbar
from app.components.sidebar import render_sidebar

def render_layout():
    render_navbar()
    render_sidebar()
    st.markdown("""
        <style>
        .custom-content {
            margin-top: 50px;
            margin-left: 70px;
            padding: 20px;
            transition: margin-left 0.3s ease;
        }
        .custom-sidebar:hover ~ .custom-content {
            margin-left: 220px;
        }
        @media screen and (max-width: 768px) {
            .custom-content {
                margin-left: 0;
            }
        }
        </style>
        <div class="custom-content">
    """, unsafe_allow_html=True)
