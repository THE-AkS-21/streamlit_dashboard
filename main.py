from app.components.navbar import render_navbar_and_sidebar
from app.utils.styles import load_css
from config import init_page_config, hide_streamlit_style
render_navbar_and_sidebar()
init_page_config()
hide_streamlit_style()
load_css()


from app.components.sidebar import render_sidebar
from pages import dashboard, analytics, settings


import streamlit as st
# Load config and hide Streamlit elements

# Use this padding container to create spacing under navbar and beside sidebar
st.markdown('<div class="custom-content">', unsafe_allow_html=True)

# Render Navbar
# render_navbar()
# render_sidebar()

# Determine current page and render accordingly
current_page = st.session_state.get("current_page", "Dashboard")

if current_page == "Dashboard":
    dashboard.show_dashboard()
elif current_page == "Analytics":
    analytics.show_analytics()
elif current_page == "Settings":
    settings.show_settings()


# st.set_page_config(
#     page_title="Business Dashboard",
#     page_icon="📊",
#     layout="wide"
# )
#
# # Load custom CSS
# st.markdown(load_css(), unsafe_allow_html=True)
#
# # def login_screen():
# #     st.header("WELCOME TO THE BSC")
# #     st.subheader("Please log in.")
# #     if st.button("Log in with Google"):
# #          st.login()
# #
# # if not st.user.is_logged_in:
# #     login_screen()
# # else:
# pg = st.navigation([
#         st.Page(dashboard.show_dashboard, title="Dashboard", icon="📊"),
#         st.Page(analytics.show_analytics, title="Analytics", icon="📈"),
#         st.Page(settings.show_settings, title="Settings", icon="⚙️"),
#     ], position="top")
#
#     # Run the selected page
# pg.run()


