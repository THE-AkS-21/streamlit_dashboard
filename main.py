import streamlit as st
from app.utils.session import SessionManager

st.set_page_config(
    page_title="Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)


def main():
    SessionManager.init_session()

    if st.session_state.get("authenticated", False):
        st.switch_page("pages/2_Dashboard.py")
    else:
        st.switch_page("pages/1_Login.py")


if __name__ == "__main__":
    main()