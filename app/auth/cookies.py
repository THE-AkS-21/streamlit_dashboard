import streamlit as st
from streamlit_cookies_controller import CookieController

# Constants
COOKIE_NAME = "jwt_token"
COOKIE_PATH = "/"
COOKIE_MAX_AGE = 30 * 24 * 60 * 60  # 30 days

# Create cookie controller instance (cached to persist across reruns)
def get_cookie_controller():
    return CookieController()

cookie_controller = get_cookie_controller()


def set_jwt_cookie(token: str, log: bool = False) -> None:
    """Set the JWT token in browser cookies."""
    cookie_controller.set(
        COOKIE_NAME,
        token,
        max_age=COOKIE_MAX_AGE,
        path=COOKIE_PATH,
        same_site="Lax"
    )
    if log:
        st.success("✅ JWT token set in cookie.")


def get_jwt_from_cookie(log: bool = False) -> str | None:
    """Retrieve the JWT token from browser cookies."""
    token = cookie_controller.get(COOKIE_NAME)

    if token:
        st.session_state.jwt_token = token
        if log:
            st.success("✅ JWT token retrieved from cookie.")
            st.code(token)
    elif log:
        st.warning("⚠️ JWT token not found in cookies.")

    return token


def clear_jwt_cookie(log: bool = False) -> None:
    """Delete the JWT cookie from browser."""
    cookie_controller.remove(COOKIE_NAME, path=COOKIE_PATH)
    if log:
        st.info("🔓 JWT cookie cleared.")
