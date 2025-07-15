import streamlit as st

from app.components.layout import render_layout
from app.config import init_page_config
from app.pages import dashboard, analytics, settings, sku_analytics
from app.constants import pages
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

def main():
    """Main application entry point"""
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
    elif current_page == pages.SKU_ANALYTICS:
        sku_analytics.show_sku_analytics()
    elif current_page == pages.SETTINGS:
        settings.show_settings()
    else:
        dashboard.show_dashboard()

    # Close content and app-container
    st.markdown("</div>", unsafe_allow_html=True)  # .custom-content
    st.markdown("</div>", unsafe_allow_html=True)  # #app-container


if __name__ == "__main__":
    main()
