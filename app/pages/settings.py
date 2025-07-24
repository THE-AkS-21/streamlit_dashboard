import streamlit as st

from app.auth.cookies import clear_jwt_cookie


def show_settings():
    # Title
    st.markdown('<h2 class="page-title">Settings</h2>', unsafe_allow_html=True)

    # Get user info from session state (or default)
    name = st.session_state.get("user_name", "Ankit Singh")
    email = st.session_state.get("user_email", "ankitt@bsc.com")
    company = st.session_state.get("user_company", "Bombay Shaving Company")
    team = st.session_state.get("user_team", "Technical")

    # Display profile card
    st.markdown(f"""
        <style>
            .profile-card {{
                background: #f0f2f6;
                padding: 1.5rem;
                top: 50%;
                left: 50%;
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
            <div class="profile-item"><strong>Name:</strong>{name}</div>
            <div class="profile-item"><strong>Email:</strong> {email} </div>
            <div class="profile-item"><strong>Company:</strong>{company}</div>
            <div class="profile-item"><strong>Team:</strong>{team}</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="button-container">', unsafe_allow_html=True)

    # if st.button("🔒 Sign out", key="signout_btn"):
    #     st.session_state.clear()
    #     st.session_state.logged_out = True
    #     st.switch_page("app/pages/login.py")
    #     st.rerun()

    if st.button("🔒 Sign out", key="signout_btn"):
        # Mark for logout and rerun — avoid clearing session state immediately
        st.session_state.logged_out = True
        st.rerun()  # Trigger rerun to clear safely on next run

    # Handle post-logout session clearing and redirection
    if st.session_state.get("logged_out"):
        st.session_state.clear()
        clear_jwt_cookie()
        st.logout()


    st.markdown('</div></div></div>', unsafe_allow_html=True)
