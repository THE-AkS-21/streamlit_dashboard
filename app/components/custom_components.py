import streamlit as st
import pandas as pd
from datetime import datetime

from app.components.charts import ChartComponent
from app.utils.formatters import Formatters
from app.utils.loader import show_loader
from streamlit_aggrid_bridge.MyAgGridComponent import render_aggrid, render_chart
from app.database.connection import db

DEFAULT_START_DATE = datetime(2025, 3, 1).date()
DEFAULT_END_DATE = datetime(2025, 4, 1).date()

def get_filtered_data(category, subcategory, sku, start_date, end_date):
    filters = {
        "start_date": start_date,
        "end_date": end_date,
    }

    base_query = """
        SELECT * FROM bsc.centraldsrdumpv2
        WHERE valuationdate BETWEEN :start_date AND :end_date
    """

    if sku != "None":
        base_query += " AND whsku = :sku"
        filters["sku"] = sku
    elif subcategory != "None":
        base_query += " AND subcategory = :subcategory"
        filters["subcategory"] = subcategory
    elif category != "None":
        base_query += " AND category = :category"
        filters["category"] = category

    return db.execute_query(base_query, filters)

class Render:
    def __init__(self):
        if st.session_state.metadata_df is None:
            st.warning("⚠️ No Data Found")
            return
        self.df = st.session_state.metadata_df.copy()

    def title(self, title):
        st.title(title)

    def grid(self):
        orders_df = self.df.copy()

        if orders_df is None or orders_df.empty:
            st.warning("⚠️ No records found for the selected range.")
            return

        tab1, tab2 = st.tabs(["DATA", "CHART"])

        with tab1:
            with show_loader("Loading data..."):
                render_aggrid(orders_df)

        with tab2:
            self.chart()

    def chart(self):
        CHART_TYPES = ["Area", "Line", "Bar", "Scatter", "Spline", "Step", "Dot", "Combo"]
        orders_df = self.df.copy()

        if orders_df is None or orders_df.empty:
            st.warning("⚠️ No records found for the selected range.")
            return

        numeric_columns = [col for col in orders_df.columns if pd.api.types.is_numeric_dtype(orders_df[col])]
        col_a, col_b, col_c = st.columns([3, 2, 3])

        with col_a:
            y1_cols = st.multiselect("Select Y-Axis 1 (Left) Columns", options=numeric_columns,
                                     default=[col for col in ["units", "offtake"] if col in numeric_columns])
        with col_b:
            chart_type = st.selectbox("Chart Type", CHART_TYPES, key="dsr_chart_type")
        with col_c:
            y2_cols = st.multiselect("Select Y-Axis 2 (Right) Columns", options=numeric_columns,
                                     default=[col for col in ["asp"] if col in numeric_columns])

        with show_loader("Loading chart..."):
            render_chart(orders_df)

    def filter(self):

        metadata_df = self.df.copy()

        categories = sorted(filter(None, metadata_df['category'].dropna().unique()))
        subcategories = sorted(filter(None, metadata_df['subcategory'].dropna().unique()))
        skus = sorted(filter(None, metadata_df['whsku'].dropna().unique()))
        last_date = DEFAULT_END_DATE

        # ─── Restore session defaults or assign ───
        start_date = st.session_state.get("filter_start", DEFAULT_START_DATE)
        end_date = st.session_state.get("filter_end", last_date)

        col1, col2, col3, col4, col5 = st.columns([1.5, 1.5, 2, 1.5, 1.5], gap="small")

        category = col1.selectbox("Category", ["None"] + categories, key="filter_category")
        subcategory = col2.selectbox("Subcategory", ["None"] + subcategories, key="filter_subcategory")
        sku = col3.selectbox("SKU", ["None"] + skus, key="filter_sku")
        start_date = col4.date_input("Start Date", value=start_date, key="filter_start")
        end_date = col5.date_input("End Date", value=end_date, key="filter_end")

        # ─── Save selected filters to session state ───
        start_date = st.session_state["filter_start"]
        end_date = st.session_state["filter_end"]

        filters = (category, subcategory, sku, start_date, end_date)
        filter_key = f"{category}_{subcategory}_{sku}_{start_date}_{end_date}"

        # if "last_filter_key" not in st.session_state or st.session_state["last_filter_key"] != filter_key:
        #     df = get_filtered_data(*filters)  # apply filters to get the df
        #
        #     # ── Convert all datetime64 columns to date ──
        #     for col in df.select_dtypes(include=["datetime64[ns]"]).columns:
        #         df[col] = df[col].dt.date
        #
        #     # st.session_state["filtered_data"] = df
        #     # st.session_state["last_filter_key"] = filter_key

        # Only update filtered data if the filter changed
        if st.session_state.get("last_filter_key") != filter_key:
            df = get_filtered_data(*filters)
            for col in df.select_dtypes(include=["datetime64[ns]"]).columns:
                df[col] = df[col].dt.date
            st.session_state.filtered_data = df
            st.session_state.last_filter_key = filter_key

    def metric(self):

        orders_df = self.df.copy()
        start_date = st.session_state.get("filter_start", datetime(2025, 3, 1))
        end_date = st.session_state.get("filter_end", datetime(2025, 4, 1))

        # ✅ Only proceed if dates are valid
        if not start_date or not end_date:
            st.warning("⚠️ Please select a valid date range first.")
            return

        num_days = (end_date - start_date).days + 1

        ChartComponent.custom_metric_cards([
            {"label": "TOTAL UNITS", "value": Formatters.number(orders_df["units"].sum())},
            {"label": "AVERAGE SELLING PRICE", "value": Formatters.number(orders_df["asp"].mean())},
            {"label": "OFFTAKE", "value": Formatters.number(orders_df["offtake"].sum())},
            {"label": "DAYS", "value": Formatters.number(num_days)},
        ])