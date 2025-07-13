import streamlit as st
import base64
import os

@st.cache_resource
def load_icon(filename):
    filepath = os.path.join("app/assets/icons", filename)
    with open(filepath, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    return f"data:image/png;base64,{encoded}"
