# pages/3_Analytics.py
import streamlit as st
from app.utils.session import SessionManager

st.set_page_config(page_title="Analytics", page_icon="📈")

# Require authentication for this page
SessionManager.require_auth()

st.title("Analytics")
# Your analytics content here