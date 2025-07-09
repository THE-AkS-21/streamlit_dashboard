import streamlit as st
from pages import dashboard, analytics, settings
from app.utils.styles import load_css

st.set_page_config(
    page_title="Business Dashboard",
    page_icon="📊",
    layout="wide"
)

# Load custom CSS
st.markdown(load_css(), unsafe_allow_html=True)

def login_screen():
    st.header("WELCOME TO THE BSC")
    st.subheader("Please log in.")
    if st.button("Log in with Google"):
         st.login()

if not st.user.is_logged_in:
    login_screen()
else:
    pg = st.navigation([
        st.Page(dashboard.show_dashboard, title="Dashboard", icon="📊"),
        st.Page(analytics.show_analytics, title="Analytics", icon="📈"),
        st.Page(settings.show_settings, title="Settings", icon="⚙️"),
    ], position="top")

    # Run the selected page
    pg.run()


