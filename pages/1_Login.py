import streamlit as st
from app.services.auth_service import AuthService
from app.utils.session import SessionManager


def show_login_page():
    # Initialize session
    session_manager = SessionManager()
    session_manager.init_session()

    # Check if already authenticated
    if st.session_state.get('authenticated', False):
        if session_manager.check_session_validity():
            st.switch_page("pages/2_Dashboard.py")
            return

    st.title("🔐 Login")

    auth_service = AuthService()

    with st.container():
        st.markdown("""
            <div style='text-align: center'>
                <h2>Welcome to Analytics Dashboard</h2>
                <p>Please sign in to continue</p>
            </div>
        """, unsafe_allow_html=True)

        if st.button("Sign in with Google", type="primary"):
            try:
                auth_url, state = auth_service.initialize_login()
                st.session_state.auth_state = state

                # Redirect to Google OAuth
                st.markdown(f'''
                    <meta http-equiv="refresh" content="0; url={auth_url}">
                    <div style='text-align: center; padding: 20px;'>
                        Redirecting to Google login...
                        <br>
                        <a href="{auth_url}" target="_self">Click here if not redirected</a>
                    </div>
                ''', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Login failed: {str(e)}")


if __name__ == "__main__":
    show_login_page()