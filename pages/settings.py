# pages/settings.py
import streamlit as st
def show_settings():
    st.title("Settings")

    st.button("Log out", on_click=st.logout)
