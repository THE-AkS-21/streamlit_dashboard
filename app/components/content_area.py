import streamlit as st

def render_content_start():
    st.markdown("""<div class="custom-content" style="margin: 0; padding: 0;">""", unsafe_allow_html=True)

def render_content_end():
    st.markdown("</div>", unsafe_allow_html=True)
