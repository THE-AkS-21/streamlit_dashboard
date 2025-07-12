import streamlit as st

def render_sidebar():
    with st.container():
        st.markdown("### 📖 Navigation")
        page = st.radio(
            "",
            ["Dashboard", "Analytics", "Settings"],
            label_visibility="collapsed"
        )
        st.session_state["current_page"] = page
