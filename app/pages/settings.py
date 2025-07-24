import streamlit as st

from app.pages.login import show_login_page


def show_settings():
    # Title
    st.markdown('<h2 class="page-title">Settings</h2>', unsafe_allow_html=True)

    # Display profile card
    st.markdown(f"""
        <style>
            .profile-card {{
                background: #f0f2f6;
                padding: 1.5rem;
                border-radius: 12px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                max-width: 400px;
            }}
            .profile-item {{
                margin: 0.5rem 0;
                font-size: 1.1rem;
            }}
        </style>

        <div class="profile-card">
            <div class="profile-item"><strong>Name:</strong> THE AKS</div>
            <div class="profile-item"><strong>Email:</strong> aks@gmail.com </div>
            <div class="profile-item"><strong>Company:</strong> Bombay Shaving Company</div>
            <div class="profile-item"><strong>Team:</strong> Technical</div>
        </div>
    """, unsafe_allow_html=True)
    #
    # # Profile card
    # st.markdown("""
    #     <div class="profile-card">
    #         <div class="profile-item"><strong>Name:</strong> Ankit Singh</div>
    #         <div class="profile-item"><strong>Email:</strong> ankitt@bsc.com</div>
    #         <div class="profile-item"><strong>Company:</strong> Bombay Shaving Company</div>
    #         <div class="profile-item"><strong>Team:</strong> Technical</div>
    #     </div>
    # """, unsafe_allow_html=True)

    st.markdown('<div class="button-container">', unsafe_allow_html=True)

    if st.button("🔒 Sign out", key="signout_btn"):
        st.session_state.clear()
        st.session_state.logged_out = True
        st.switch_page("app/pages/login.py")
        st.rerun()

    st.markdown('</div></div></div>', unsafe_allow_html=True)
