# app/pages/login.py
import streamlit as st
from app.api.user_api import authenticate_user
from app.auth.cookies import clear_jwt_cookie, set_jwt_cookie


def show_login_page():
    st.title("🔐 Login")
    user_email = "lakshay@bombayshavingcompany.com"

    if st.session_state.get("login_error"):
        st.error("❌ Login failed. Please try again.")
        st.session_state.login_error = False  # Reset error

    if st.session_state.get("logged_out"):
        st.success("✅ Successfully logged out.")
        st.session_state.logged_out = False  # Reset message

    if st.button("Sign in with Google"):
        st.login()

        # Check if user is logged in (after rerun)
    if st.user and st.user.email:
        # Authenticate using backend API
        token = authenticate_user(user_email)
        if token:
            st.session_state.jwt_token = token
            st.success("✅ Token retrieved successfully!")

        else:
            st.error("❌ Authentication failed!")

        if st.session_state.get("jwt_token"):
            if st.button("continue"):
                st.switch_page("main.py")

