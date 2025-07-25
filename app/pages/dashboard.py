from datetime import datetime
import streamlit as st
import pandas as pd

from app.auth.cookies import get_jwt_from_cookie
from app.components.aggrid_renderer import render_aggrid
from app.database.connection import db
from app.database.queries.dashboard_queries import DashboardQueries
from app.components.charts import ChartComponent
from app.utils.formatters import Formatters
from app.utils.global_css import apply_global_styles
from app.utils.loader import show_loader

CHART_TYPES = ["Area"]

@st.cache_data(ttl=3600, show_spinner=False)
def _load_dashboard_metadata():
    return db.execute_query(DashboardQueries.GET_DASHBOARD_FILTER_METADATA)

def get_dashboard_metadata():
    if "dashboard_metadata" not in st.session_state:
        loader = show_loader("Loading metadata...")
        st.session_state.dashboard_metadata = _load_dashboard_metadata()
        loader.empty()
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

    col1, col2, col3, col4, col5 = st.columns([1.5, 1.5, 2, 1.5, 1.5], gap="small")

    category = col1.selectbox("Category", ["None"] + categories, key="filter_category")
    subcategory = col2.selectbox("Subcategory", ["None"] + subcategories, key="filter_subcategory")
    sku = col3.selectbox("SKU", ["None"] + skus, key="filter_sku")
    start_date = col4.date_input("Start Date", value=datetime(2025, 3, 1), key="filter_start")
    end_date = col5.date_input("End Date", value=last_date, key="filter_end")

    return category, subcategory, sku, start_date, end_date

def render_dashboard_data(df, start_date, end_date):

    orders_df = df
    token = get_jwt_from_cookie()
    st.write(f"Token: {token}")
    if orders_df is None or orders_df.empty:
        st.warning("⚠️ No records found for the selected range.")
        return

    if "value" not in orders_df.columns:
        orders_df["value"] = orders_df.get("units", 0)

    # ─── Metrics ───
    num_days = (end_date - start_date).days + 1
    ChartComponent.metric_cards([
        {"label": "Total Units", "value": Formatters.number(orders_df["value"].sum())},
        {"label": "Avg Daily Units", "value": Formatters.number(orders_df["value"].sum() / num_days)},
        {"label": "Days", "value": Formatters.number(num_days)},
    ])

    # ─── AG Grid ───
    st.markdown("#### AG-Grid")
    render_aggrid(orders_df)

    # ─── Chart Controls ───
    st.markdown("#### Chart")
    numeric_columns = [col for col in orders_df.columns if pd.api.types.is_numeric_dtype(orders_df[col])]
    col_a, col_b = st.columns([4, 2])

    with col_a:
        selected_columns = st.multiselect(
            "Select Columns", options=numeric_columns,
            default=["asp", "units", "offtake"],
            key="select_columns"
        )
    with col_b:
        chart_type = st.selectbox("Chart Type", CHART_TYPES, key="dsr_chart_type")

    # ─── Render Chart when filters change ───
    chart_df_key = f"chart_df_{'_'.join(selected_columns)}_{chart_type}"
    if chart_df_key not in st.session_state:
        valuation_dates = pd.to_datetime(orders_df.get("valuationdate"), errors="coerce")
        df = pd.DataFrame({"valuationdate": valuation_dates})
        for col in selected_columns:
            df[col] = pd.to_numeric(orders_df.get(col, []), errors="coerce")
        df.dropna(subset=["valuationdate"] + selected_columns, inplace=True)
        st.session_state[chart_df_key] = df

    df = st.session_state[chart_df_key]

    if df.empty:
        st.warning("⚠️ Data is empty after cleanup.")
        return

    chart_component = ChartComponent(df)

    if chart_type == "Area":
        chart_component.multi_metric_time_series(
            x_axis="valuationdate",
            key="multi_metric"
        )
    else:
        melted_df = df.melt(id_vars=["valuationdate"], var_name="metric", value_name="value")
        ChartComponent(melted_df).render_dynamic_chart(
            x_axis="valuationdate",
            y_axis="value",
            chart_type=chart_type
        )

    # ─── Download Button ───
    st.download_button(
        label="📥 Download CSV",
        data=df.to_csv(index=False),
        file_name="chart_data.csv",
        mime="text/csv",
        use_container_width=True
    )

def show_dashboard():
    apply_global_styles()

    metadata_df = get_dashboard_metadata()
    filters = render_filter_form(metadata_df)

    filter_key = f"{filters[0]}_{filters[1]}_{filters[2]}_{filters[3]}_{filters[4]}"

    if "last_filter_key" not in st.session_state or st.session_state["last_filter_key"] != filter_key:
        loader = show_loader("Fetching filtered data...")
        df = get_filtered_data(*filters)
        st.session_state["filtered_data"] = df
        st.session_state["last_filter_key"] = filter_key
        loader.empty()

    df = st.session_state.get("filtered_data", pd.DataFrame())
    render_dashboard_data(df, filters[3], filters[4])
