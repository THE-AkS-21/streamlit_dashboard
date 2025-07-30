from datetime import datetime
import streamlit as st
import pandas as pd

from app.components.aggrid_renderer import render_aggrid
from app.database.connection import db
from app.database.queries.dashboard_queries import DashboardQueries
from app.components.charts import ChartComponent
from app.utils.formatters import Formatters
from app.utils.global_css import apply_global_styles
from app.utils.loader import show_loader

CHART_TYPES = ["Area", "Line", "Bar", "Scatter", "Spline", "Step", "Dot", "Combo"]

@st.cache_data(ttl=3600, show_spinner=False)
def _load_dashboard_metadata():
    return db.execute_query(DashboardQueries.GET_DASHBOARD_FILTER_METADATA)

def get_dashboard_metadata():
    if "dashboard_metadata" not in st.session_state:
        st.session_state.dashboard_metadata = _load_dashboard_metadata()
    return st.session_state.dashboard_metadata

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

def render_filter_form(metadata_df):
    categories = sorted(filter(None, metadata_df['category'].dropna().unique()))
    subcategories = sorted(filter(None, metadata_df['subcategory'].dropna().unique()))
    skus = sorted(filter(None, metadata_df['sku'].dropna().unique()))
    last_date = metadata_df['last_date'].max()

    with st.popover("FILTERS"):

        col1, col2, col3, col4, col5 = st.columns([1.5, 1.5, 2, 1.5, 1.5], gap="small")

        category = col1.selectbox("Category", ["None"] + categories, key="filter_category")
        subcategory = col2.selectbox("Subcategory", ["None"] + subcategories, key="filter_subcategory")
        sku = col3.selectbox("SKU", ["None"] + skus, key="filter_sku")
        start_date = col4.date_input("Start Date", value=datetime(2025, 3, 1), key="filter_start")
        end_date = col5.date_input("End Date", value=last_date, key="filter_end")

        return category, subcategory, sku, start_date, end_date

def render_chart_data(df):
    orders_df = df
    if orders_df is None or orders_df.empty:
        st.warning("⚠️ No records found for the selected range.")
        return

    tab1, tab2 = st.tabs(["DATA", "CHART"])

    with tab1:
        with show_loader("Loading data..."):
            render_aggrid(orders_df)

    with tab2:
        numeric_columns = [col for col in orders_df.columns if pd.api.types.is_numeric_dtype(orders_df[col])]
        col_a, col_b, col_c = st.columns([3, 2, 3])

        with col_a:
            y1_cols = st.multiselect("Select Y-Axis 1 (Left) Columns", options=numeric_columns, default=[col for col in ["units", "offtake"] if col in numeric_columns])
        with col_b:
            chart_type = st.selectbox("Chart Type", CHART_TYPES, key="dsr_chart_type")
        with col_c:
            y2_cols = st.multiselect("Select Y-Axis 2 (Right) Columns", options=numeric_columns, default=[col for col in ["asp"] if col in numeric_columns])

        if df.empty:
            st.warning("⚠️ Data is empty after cleanup.")
            return

        # chart_component = ChartComponent(df)
        with show_loader("Loading chart..."):
            ChartComponent(df).multi_yaxis_line_chart("valuationdate", y1_cols, y2_cols)
        # ChartComponent(df).multi_yaxis_chart("valuationdate", y1_cols, y2_cols, plot_type=chart_type)

def render_metrics(df, start_date, end_date):

    orders_df = df
    if orders_df is None or orders_df.empty:
        st.warning("⚠️ No records found for the selected range.")
        return

    # if "metric_units" not in orders_df.columns:
    #     orders_df["metric_units"] = orders_df.get("units", 0)
    # if "metric_asp" not in orders_df.columns:
    #     orders_df["metric_asp"] = orders_df.get("asp", 0)
    # if "metric_offtake" not in orders_df.columns:
    #     orders_df["metric_offtake"] = orders_df.get("offtake", 0)

    # ─── Metrics ───
    num_days = (end_date - start_date).days + 1

    ChartComponent.metric_cards([
        {"label": "TOTAL UNITS", "value": Formatters.number(orders_df["units"].sum())},
        {"label": "AVERAGE SELLING PRICE", "value": Formatters.number(orders_df["asp"].mean())},
        {"label": "OFFTAKE", "value": Formatters.number(orders_df["offtake"].sum())},
        {"label": "DAYS", "value": Formatters.number(num_days)},
    ])

def render_metric_chart(df, chart_type):
    if df is None or df.empty:
        st.error("No Data Found.")
        return

    df["valuationdate"] = pd.to_datetime(df["valuationdate"])

    if chart_type == "bar":
        # Aggregate units as sum per valuationdate
        chart_df = (
            df.groupby("valuationdate")[["units"]]
            .sum()
            .reset_index()
        )
        y_axis = ["units"]
        ChartComponent(chart_df).metric_bar_chart("valuationdate", y_axis)

    elif chart_type == "line":
        # Aggregate asp as mean per valuationdate
        chart_df = (
            df.groupby("valuationdate")[["asp"]]
            .mean()
            .reset_index()
        )
        y_axis = ["asp"]
        ChartComponent(chart_df).metric_line_chart("valuationdate", y_axis)


def show_dashboard():
    apply_global_styles()

    metadata_df = get_dashboard_metadata()

    col_1, col_2 = st.columns([1, 3])

    with col_1:
        # ── Inner Columns for Uniform Filter Layout ──
        f_col1, f_col2, f_col3 = st.columns(3)

        # ── Filter Form ──
        with f_col1:
            filters = render_filter_form(metadata_df)

        # ── Group By Dropdown ──
        with f_col2:
            group_by_option = st.selectbox(
                label="",
                options=["Day", "Month", "Year"],
                index=0,
                key="group_by"
            )

        # ── Download Button ──
        with f_col3:
            download_btn_placeholder = st.empty()

        filter_key = f"{filters[0]}_{filters[1]}_{filters[2]}_{filters[3]}_{filters[4]}"

        if "last_filter_key" not in st.session_state or st.session_state["last_filter_key"] != filter_key:
            df = get_filtered_data(*filters)  # apply filters to get the df

            # ── Convert all datetime64 columns to date ──
            for col in df.select_dtypes(include=["datetime64[ns]"]).columns:
                df[col] = df[col].dt.date

            st.session_state["filtered_data"] = df
            st.session_state["last_filter_key"] = filter_key

        df = st.session_state.get("filtered_data", pd.DataFrame())

        # Place download button (only if df is not empty)
        if not df.empty:
            csv = df.to_csv(index=False).encode("utf-8")
            download_btn_placeholder.download_button(
                label=" Download ",
                data=csv,
                file_name="filtered_data.csv",
                mime="text/csv",
                key="download_csv_btn"
            )

        render_metrics(df, filters[3], filters[4])

    with col_2:
        tab1, tab2 = st.tabs(["UNITS", "ASP"])

        with tab1:
            with show_loader("Loading metric chart..."):
                render_metric_chart(df, "bar")

        with tab2:
            with show_loader("Loading metric chart..."):
                render_metric_chart(df, "line")

    render_chart_data(df)
