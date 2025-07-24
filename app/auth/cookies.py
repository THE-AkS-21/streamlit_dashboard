import uuid
import streamlit as st
from streamlit_javascript import st_javascript

def set_jwt_cookie(token: str):
    st_javascript(f"""
        document.cookie = "jwt_token={token}; path=/; max-age={30*24*60*60}; SameSite=Lax";
    """)

def get_jwt_from_cookie():
    token = st_javascript("""
        const value = document.cookie
            .split('; ')
            .find(row => row.startsWith('jwt_token='));
        return value ? value.split('=')[1] : null;
    """, key=f"get_jwt_token_js_{uuid.uuid4()}")  # Unique key per call

    if token:
        st.session_state.jwt_token = token
        st.write("✅ TOKEN FROM COOKIE:", token)
    else:
        st.warning("⚠️ JWT token not found in cookie.")

    return token

def clear_jwt_cookie():
    st_javascript(
        """
        document.cookie = "jwt_token=; path=/; max-age=0; expires=Thu, 01 Jan 1970 00:00:00 UTC; SameSite=Lax";
        """,
        key=f"clear_jwt_cookie_{uuid.uuid4()}"  # Generate a unique key on each call
    )


