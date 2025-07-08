# app/pages/login.py
import streamlit as st
from app.services.auth_service import AuthService
from app.utils.session import set_authenticated_user


def show_login_page():
    st.title("🔐 Login")

    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button("Login")

            if submit_button:
                auth_service = AuthService()
                if auth_service.verify_credentials(username, password):
                    set_authenticated_user(username)
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")