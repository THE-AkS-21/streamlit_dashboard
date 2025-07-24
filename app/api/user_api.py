# app/api/user_api.py
import os
from dotenv import load_dotenv
import requests
import streamlit as st
from app.auth.cookies import set_jwt_cookie

# Cache API URL at session level
@st.cache_resource
def get_api_url():
    secret_api_url = st.secrets["api"]["API_URL"]
    if secret_api_url:
        return secret_api_url

def authenticate_user(email: str) -> str | None:
    api_url = get_api_url()
    if not api_url:
        return None

    # HEADERS
    # headers = {
    #     "X-Origin":"Streamlit",
    #     "X-User": email
    # }
    # PAYLOAD
    payload = {
        "tenantId": 1,
        "email": email,
        "isSignInWithGoogle": True
    }
    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status()

        data = response.json()
        token = data

        if not token:
            st.warning("🟡 Authentication succeeded but no token returned.")
            return None

        #Setting Cookie in token when successfully received
        set_jwt_cookie(token)
        return token

    except requests.RequestException as e:
        st.error(f"🔴 API Error: {e}")
        st.exception(e)
        return None
