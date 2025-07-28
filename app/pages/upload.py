import streamlit as st
import pandas as pd
import time
from app.components.aggrid_renderer import render_aggrid

def show_upload():
    st.title("IMPORT")
    # Upload file
    uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

    # Handle file
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith(".xlsx"):
                df = pd.read_excel(uploaded_file)
            else:
                st.error("Unsupported file type.")
                df = None

            if df is not None:
                st.success("✅ File uploaded successfully!")
                st.markdown('<div class="analytics-container">', unsafe_allow_html=True)
                start_time = time.time()
                render_aggrid(df)
                duration = time.time() - start_time
                st.success(f"✅ Data fetched in {duration:.2f} seconds")
                st.markdown('</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"❌ Error reading file: {e}")
