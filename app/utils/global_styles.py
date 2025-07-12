import streamlit as st

def inject_global_css():
    st.markdown("""
        <style>
        /* Remove default padding from Streamlit’s main block container */
        section.main > div.block-container {
            padding-top: 0rem !important;
        }
        /* Also reset margin/padding around markdown headers globally */
        [data-testid="stMarkdownContainer"] {
            margin-top: 0 !important;
            margin-bottom: 0 !important;
            padding-top: 0 !important;
            padding-bottom: 0 !important;
        }
        h1, h2, h3, h4, h5, h6 {
            margin-top: 0 !important;
        }
        </style>
    """, unsafe_allow_html=True)

def remove_default_spacing():
    st.markdown("""
        <style>
        /* Remove default padding from Streamlit’s container */
        section.main > div.block-container {
            padding-top: 0rem !important;
        }
        /* Remove padding/margins from markdown blocks */
        [data-testid="stMarkdownContainer"] {
            margin-top: 0rem !important;
            padding-top: 0rem !important;
        }
        h1, h2, h3, h4, h5, h6 {
            margin-top: 0rem !important;
        }
        </style>
    """, unsafe_allow_html=True)

def remove_streamlit_padding():
    st.markdown("""
        <style>
        section.main > div.block-container {
            padding-top: 0rem !important;
        }
        [data-testid="stMarkdownContainer"] {
            margin-top: 0 !important;
            padding-top: 0 !important;
        }
        h1, h2, h3, h4, h5, h6 {
            margin-top: 0 !important;
        }
        </style>
    """, unsafe_allow_html=True)

def remove_all_top_spacing():
    st.markdown("""
        <style>
        html, body {
            padding-top: 0 !important;
            margin-top: 0 !important;
        }
        main {
            padding-top: 0px !important;
            margin-top: 0px !important;
        }
        section.main {
            padding-top: 0px !important;
            margin-top: 0px !important;
        }
        section.main > div.block-container {
            padding-top: 0px !important;
            margin-top: 0px !important;
        }
        [data-testid="stAppViewContainer"] {
            padding-top: 0px !important;
            margin-top: 0px !important;
        }
        [data-testid="stVerticalBlock"],
        [data-testid="stHorizontalBlock"],
        [data-testid="stMarkdownContainer"] {
            padding-top: 0px !important;
            margin-top: 0px !important;
        }
        h1, h2, h3, h4, h5, h6 {
            padding-top: 0px !important;
            margin-top: 0px !important;
        }
        </style>
    """, unsafe_allow_html=True)
