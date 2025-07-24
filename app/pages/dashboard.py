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

CHART_TYPES = ["Area"]

# ────────────────────────────────
# Caching with Session Integration
# ────────────────────────────────

@st.cache_data(ttl=3600)
def _get_dashboard_metadata():
    return db.execute_query(DashboardQueries.GET_DASHBOARD_FILTER_METADATA)

def get_dashboard_metadata():
    if "dashboard_metadata" not in st.session_state:
        loader = show_loader("Loading filter metadata...")
        st.session_state.dashboard_metadata = _get_dashboard_metadata()
        loader.empty()
    return st.session_state.dashboard_metadata

@st.cache_data(ttl=3600)
def _get_all_data(start_date, end_date):
    return db.execute_query(DashboardQueries.GET_DASHBOARD_CHART_DATA, {
        "start_date": start_date,
        "end_date": end_date
    })

def get_all_data(start_date, end_date):
    cache_key = f"all_data_{start_date}_{end_date}"
    if cache_key not in st.session_state:
        loader = show_loader("Loading data...")
        st.session_state[cache_key] = _get_all_data(start_date, end_date)
        loader.empty()
    return st.session_state[cache_key]

@st.cache_data(ttl=3600)
def _get_filtered_data(start_date, end_date, category, subcategory, sku):
    filters = []
    params = {"start_date": start_date, "end_date": end_date}

    if sku and sku != "None":
        filters.append("AND whsku = :sku")
        params["sku"] = sku
    if category and category != "None":
        filters.append("AND category = :category")
        params["category"] = category
    if subcategory and subcategory != "None":
        filters.append("AND subcategory = :subcategory")
        params["subcategory"] = subcategory

    filter_clause = "\n        ".join(filters)
    query = DashboardQueries.GET_DASHBOARD_FILTERED_CHART_DATA.replace("{filters}", filter_clause)

    return db.execute_query(query, params)

@st.cache_data(ttl=3600)
def get_filtered_data(start_date, end_date, category=None, subcategory=None, sku=None):
    cache_key = f"filtered_{start_date}_{end_date}_{category}_{subcategory}_{sku}"
    if cache_key not in st.session_state:
        loader = show_loader("Loading filtered data...")
        st.session_state[cache_key] = _get_filtered_data(start_date, end_date, category, subcategory, sku)
        loader.empty()
    return st.session_state[cache_key]

@st.cache_data(ttl=3600)
def run_dashboard_query(sku, start_date, end_date):
    query = DashboardQueries.MONTHLY_ORDERS_WITH_SKU if sku != "None" else DashboardQueries.MONTHLY_ORDERS_NO_SKU
    params = {"start_date": start_date, "end_date": end_date}
    if sku != "None":
        params["whsku"] = sku
    return query, params, db.execute_query(query, params)

def render_filter_form(metadata_df):
    loader = show_loader("Loading filter form...")

    categories = sorted(filter(None, metadata_df['category'].unique()))
    subcategories = sorted(filter(None, metadata_df['subcategory'].unique()))
    skus = sorted(filter(None, metadata_df['sku'].unique()))
    last_date = metadata_df['last_date'].max()

    col1, col2, col3, col4, col5 = st.columns([1.5, 1.5, 2, 1.5, 1.5], gap="small")

    category = col1.selectbox("Category", ["None"] + categories, key="filter_category")
    subcategory = col2.selectbox("Subcategory", ["None"] + subcategories, key="filter_subcategory")
    sku = col3.selectbox("SKU", ["None"] + skus, key="filter_sku")
    start_date = col4.date_input("Start Date", value=datetime(2025, 3, 1), key="filter_start")
    end_date = col5.date_input("End Date", value=last_date, key="filter_end")

    loader.empty()
    return category, subcategory, sku, start_date, end_date

def render_report_tabs(start_date, end_date):
    tabs = st.tabs(st.session_state.report_tabs)

    for i, tab_name in enumerate(st.session_state.report_tabs):
        orders_df = st.session_state.report_data.get(tab_name)
        if orders_df is None or orders_df.empty:
            continue

        with tabs[i]:
            # ─── Header ───
            col1, col2 = st.columns([10, 1])
            col1.markdown(f"### {tab_name}")
            if col2.button("❌", key=f"close_{tab_name}", use_container_width=True):
                st.session_state.report_tabs.remove(tab_name)
                st.session_state.report_data.pop(tab_name)
                st.rerun()

            # ─── Metric Cards ───
            if "value" not in orders_df.columns:
                orders_df["value"] = orders_df.get("units", 0)

            ChartComponent.metric_cards([
                {"label": "Total Units", "value": Formatters.number(orders_df["value"].sum())},
                {"label": "Avg Daily Units", "value": Formatters.number(orders_df["value"].mean())},
                {"label": "Days", "value": Formatters.number(len(orders_df))}
            ])

            # ─── AG-Grid ───
            st.markdown("#### AG-Grid")
            data_df = get_all_data(start_date, end_date)
            if data_df.empty:
                st.warning("⚠️ No records found for the selected range and page.")
                continue

            render_aggrid(data_df)

            # ─── Chart Inputs ───
            numeric_columns = [col for col in data_df.columns if pd.api.types.is_numeric_dtype(data_df[col])]

            col_a, col_b, col_c, col_d = st.columns([3, 2, 1, 2])
            with col_a:
                selected_columns = st.multiselect(
                    "Select Columns",
                    options=numeric_columns,
                    default=["asp","units","offtake"],
                    key=f"{tab_name}_select_columns"
                )

            with col_b:
                chart_type = st.selectbox(
                    "Chart Type",
                    CHART_TYPES,
                    key=f"{tab_name}_chart_type"
                )

            with col_c:
                st.markdown("###")  # vertical align
                plot_clicked = st.button("Plot", key=f"plot_chart_btn_{tab_name}", use_container_width=True)

            with col_d:
                st.markdown("###")
                download_placeholder = st.empty()

            # ─── Handle Chart ───
            if plot_clicked:
                st.markdown("#### Chart")

                if not selected_columns:
                    st.warning("⚠️ Please select at least one numeric column to plot.")
                    st.stop()

                # ─── Prepare Chart Data ───
                valuation_dates = pd.to_datetime(data_df.get("valuationdate"), errors="coerce")
                df = pd.DataFrame({"valuationdate": valuation_dates})

                for col in selected_columns:
                    df[col] = pd.to_numeric(data_df.get(col, []), errors="coerce")

                df.dropna(subset=["valuationdate"] + selected_columns, inplace=True)

                if df.empty:
                    st.warning("⚠️ Data is empty or invalid after cleanup.")
                    st.stop()

                st.session_state[f"{tab_name}_chart_df"] = df
                st.session_state[f"{tab_name}_chart_rendered"] = True

                chart_component = ChartComponent(df)

                if chart_type in ["Area"]:
                    chart_component.multi_metric_time_series(
                        x_axis="valuationdate",
                        key=f"{tab_name}_multi_metric"
                    )
                else:
                    melted_df = df.melt(id_vars=["valuationdate"], var_name="metric", value_name="value")
                    ChartComponent(melted_df).render_dynamic_chart(
                        x_axis="valuationdate",
                        y_axis="value",
                        chart_type=chart_type
                    )

                # ─── Download CSV ───
                download_placeholder.download_button(
                    label="📥 Download CSV",
                    data=df.to_csv(index=False),
                    file_name=f"{tab_name}_chart_data.csv",
                    mime="text/csv",
                    use_container_width=True
                )

def show_dashboard():
    apply_global_styles()
    st.session_state.setdefault("report_tabs", [])
    st.session_state.setdefault("report_data", {})
    st.session_state.setdefault("last_filters", {})

    metadata_df = get_dashboard_metadata()
    category, subcategory, sku, start_date, end_date = render_filter_form(metadata_df)

    current_filters = {
        "category": category,
        "subcategory": subcategory,
        "sku": sku,
        "start_date": start_date,
        "end_date": end_date,
    }

    filters_changed = current_filters != st.session_state["last_filters"]

    if filters_changed:
        # Fetch filtered or unfiltered data
        if (category, subcategory, sku) == ("None", "None", "None"):
            df = get_all_data(start_date, end_date)
        else:
            df = get_filtered_data(start_date, end_date, category, subcategory, sku)

        st.session_state["last_filters"] = current_filters
        st.session_state["report_data"] = { "Central DSR": df }

    # Always show latest chart data
    st.session_state["report_tabs"] = ["Central DSR"]
    render_report_tabs(start_date, end_date)



