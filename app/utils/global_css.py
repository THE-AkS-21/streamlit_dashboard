import streamlit as st

def apply_global_styles():
    st.markdown("""
        <style>
        html, body, main, section.main, section.main > div.block-container,
        [data-testid="stAppViewContainer"],
        [data-testid="stVerticalBlock"],
        [data-testid="stHorizontalBlock"],
        [data-testid="stMarkdownContainer"] {
            margin-top: 0 !important;
            padding-top: 0 !important;
        }
        h1, h2, h3, h4, h5, h6 {
            margin-top: 0 !important;
        }
        </style>
    """, unsafe_allow_html=True)
