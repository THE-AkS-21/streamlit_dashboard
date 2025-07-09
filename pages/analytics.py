# pages/analytics.py
import streamlit as st
def show_analytics():
    st.title("Analytics")

    st.button("Log out", on_click=st.logout)
