import streamlit as st

from app.auth.cookies import get_jwt_from_cookie
from app.auth.jwt_manager import decode_jwt
from app.components.layout import render_layout
from app.config import init_page_config
from app.pages import dashboard, analytics, settings, sku_analytics, upload, pnl_analytics
from app.constants import pages
from app.pages.login import show_login_page
from app.utils.global_css import apply_global_styles

# Initialize config
init_page_config()
# Apply global styles
apply_global_styles()

def get_current_page():
    """Get current page from URL parameters or session state"""
    query_params = st.query_params
    if 'page' in query_params:
        page = query_params['page']
        st.session_state.current_page = page
        return page
    return st.session_state.get("current_page", pages.DASHBOARD)

def authenticate_from_cookie() -> bool:
    """Check JWT in cookie, decode and set session if valid."""
    token = get_jwt_from_cookie()
    if not token:
        return False

    # payload = decode_jwt(token)
    # if not payload:
    #     return False
    #
    # # Set session state with user info if not already set
    # st.session_state.jwt_token = token
    # st.session_state.user_email = payload.get("email")
    # st.session_state.user_role = payload.get("role")
    return True

def main():
    """Main application entry point"""
    if not authenticate_from_cookie():
        show_login_page()
        st.stop()

    st.markdown(
        """<div id="app-container" style="margin: 0; padding: 0;">""",
        unsafe_allow_html=True
    )

    render_layout()  # renders navbar + sidebar

    # Open content wrapper once here
    st.markdown(
        """<div class="custom-content" style="margin: 0; padding: 0;">""",
        unsafe_allow_html=True
    )

    # Get current page and render respective page content inside custom-content
    current_page = get_current_page()

    if current_page == pages.DASHBOARD:
        dashboard.show_dashboard()
    elif current_page == pages.ANALYTICS:
        analytics.show_analytics()
    elif current_page == pages.SETTINGS:
        settings.show_settings()
    else:
        dashboard.show_dashboard()

    # Close content and app-container
    st.markdown("</div>", unsafe_allow_html=True)  # .custom-content
    st.markdown("</div>", unsafe_allow_html=True)  # #app-container


if __name__ == "__main__":
    main()
