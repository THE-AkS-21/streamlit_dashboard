import streamlit as st
from app.services.auth_service import AuthService
from app.utils.session import SessionManager


def handle_callback():
    st.set_page_config(
        page_title="Authentication Callback",
        page_icon="🔒",
        initial_sidebar_state="collapsed"
    )

    # Hide all navigation elements
    st.markdown("""
        <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)

    auth_service = AuthService()
    session_manager = SessionManager()

    # Initialize session
    session_manager.init_session()

    # Get query parameters
    query_params = st.query_params

    if "code" in query_params and "state" in query_params:
        try:
            # Verify state matches
            stored_state = st.session_state.get("auth_state")
            if not stored_state or stored_state != query_params["state"]:
                raise Exception("Invalid state parameter")

            # Process callback
            user_info = auth_service.handle_callback(
                query_params["state"],
                query_params["code"]
            )

            if user_info:
                # Clear query parameters
                st.query_params.clear()
                # Redirect to dashboard
                st.switch_page("pages/2_Dashboard.py")
            else:
                raise Exception("Failed to get user information")

        except Exception as e:
            st.error(f"Authentication failed: {str(e)}")
            # Wait briefly before redirecting
            st.markdown("""
                <meta http-equiv="refresh" content="3; url=/login">
                Redirecting to login page...
            """, unsafe_allow_html=True)
    else:
        st.error("Missing authentication parameters")
        # Wait briefly before redirecting
        st.markdown("""
            <meta http-equiv="refresh" content="3; url=/login">
            Redirecting to login page...
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    handle_callback()