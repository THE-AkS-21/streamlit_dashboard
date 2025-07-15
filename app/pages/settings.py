import streamlit as st

def show_settings():
    # Page container inside custom-content
    st.markdown(
        """<div class="custom-content"><div class="settings-container">""",
        unsafe_allow_html=True
    )

    # Title
    st.markdown('<h2 class="page-title">Settings</h2>', unsafe_allow_html=True)

    # Profile card
    st.markdown("""
        <div class="profile-card">
            <div class="profile-item"><strong>Name:</strong> Ankit Singh</div>
            <div class="profile-item"><strong>Email:</strong> ankitt@bsc.com</div>
            <div class="profile-item"><strong>Company:</strong> Bombay Shaving Company</div>
            <div class="profile-item"><strong>Team:</strong> Technical</div>
        </div>
    """, unsafe_allow_html=True)

    # Button container
    st.markdown('<div class="button-container">', unsafe_allow_html=True)

    if st.button("🔒 Sign out", key="signout_btn"):
        st.cache_data.clear()
        st.cache_resource.clear()
        st.session_state.clear()
        st.rerun()

    # Close button-container, settings-container and custom-content
    st.markdown('</div></div></div>', unsafe_allow_html=True)
