import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from app.config import AppConfig

def show_dashboard():
    # Load CSV
    df = pd.read_csv("business-price-indexes-march-2025.csv")

    # Convert Period to datetime (safe)
    df["Period"] = pd.to_datetime(df["Period"], format='mixed', errors='coerce')  # invalid dates to NaT

    # Drop rows where Period couldn't be parsed
    df = df.dropna(subset=["Period"])

    # Extract available years
    df["Year"] = df["Period"].dt.year
    years = df["Year"].unique()

    st.title("📊 Capital Goods Price Index Dashboard")

    # If at least 2 years available, show slider
    if len(years) >= 2:
        min_year = int(df["Year"].min())
        max_year = int(df["Year"].max())

        start_year, end_year = st.sidebar.slider("Select Year Range:",
                                                 min_value=min_year,
                                                 max_value=max_year,
                                                 value=(min_year, max_year))

        # Filter by selected year range
        filtered_df = df[(df["Year"] >= start_year) & (df["Year"] <= end_year)]
    else:
        st.sidebar.warning("Not enough year data for range selection. Showing all data.")
        filtered_df = df

    # Show filtered data
    st.subheader("Capital Goods Price Index Data")
    st.dataframe(filtered_df[["Period", "Data_value"]])

    # Line chart
    st.subheader("📈 Price Index Trend")
    if not filtered_df.empty:
        st.line_chart(filtered_df.set_index("Period")["Data_value"])
    else:
        st.info("No data available for selected period.")

    st.button("Log out", on_click=st.logout)
