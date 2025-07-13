import streamlit as st
from app.components.layout import render_layout
from app.components.sidebar_toggle_script import render_sidebar_toggle_script
from app.pages import dashboard, analytics, settings
from app.constants import pages
from app.utils.global_css import apply_global_styles
from config import init_page_config

# Initialize config
init_page_config()

# Apply global styles
apply_global_styles()


def get_current_page():
    """Get current page from URL parameters or session state"""
    # Check URL parameters first
    query_params = st.query_params
    if 'page' in query_params:
        page = query_params['page']
        st.session_state.current_page = page
        return page

    # Fall back to session state
    return st.session_state.get("current_page", pages.DASHBOARD)


def main():
    """Main application entry point"""
    # Render layout (navbar + sidebar)
    render_layout()
    # Sidebar JS functionality (called after both have rendered)
    render_sidebar_toggle_script()

    # Get current page
    current_page = get_current_page()

    # Route to appropriate page
    if current_page == pages.DASHBOARD:
        dashboard.show_dashboard()
    elif current_page == pages.ANALYTICS:
        analytics.show_analytics()
    elif current_page == pages.SETTINGS:
        settings.show_settings()
    else:
        # Default to dashboard if page not found
        dashboard.show_dashboard()


if __name__ == "__main__":
    main()