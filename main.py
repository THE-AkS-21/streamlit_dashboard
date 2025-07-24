import streamlit as st

from app.auth.cookies import get_jwt_from_cookie
from app.auth.jwt_manager import decode_jwt
from app.components.layout import render_layout
from app.config import init_page_config
from app.constants import pages
from app.pages import dashboard, analytics, settings
from app.pages.login import show_login_page
from app.utils.global_css import apply_global_styles


def init_app():
    """Initializes page config and global styles"""
    init_page_config()
    apply_global_styles()


def get_current_page() -> str:
    """Returns the current page from query params or session"""
    query_params = st.query_params
    if "page" in query_params:
        st.session_state.current_page = query_params["page"]
    return st.session_state.get("current_page", pages.DASHBOARD)


def authenticate_from_cookie() -> bool:
    """Checks JWT token and populates session if valid"""
    token = get_jwt_from_cookie()
    if not token:
        return False

    # Uncomment to validate token and populate session
    # payload = decode_jwt(token)
    # if not payload:
    #     return False
    #
    # st.session_state.jwt_token = token
    # st.session_state.user_email = payload.get("email")
    # st.session_state.user_role = payload.get("role")

    return True


def render_page(page_name: str):
    """Renders the main content based on current page"""
    if page_name == pages.DASHBOARD:
        dashboard.show_dashboard()
    elif page_name == pages.ANALYTICS:
        analytics.show_analytics()
    elif page_name == pages.SETTINGS:
        settings.show_settings()
    else:
        dashboard.show_dashboard()  # fallback


def main():
    init_app()

    # Handle login check
    if 'is_logged_in' not in st.session_state:
        if not authenticate_from_cookie():
            show_login_page()
            st.stop()

    # App container
    # st.markdown('<div id="app-container" style="margin: 0; padding: 0;">', unsafe_allow_html=True)

        # App container + custom-content wrapper in a single tag
    st.markdown(
        """<div id="app-container" style="margin: 0; padding: 0;">
               <div class="custom-content">""",
        unsafe_allow_html=True
    )
    render_layout()  # Navbar + Sidebar

    # # Main content area
    # st.markdown('<div class="custom-content" style="margin: 0; padding: 0;">', unsafe_allow_html=True)

    current_page = get_current_page()
    render_page(current_page)

    # Close divs
    st.markdown('</div></div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
