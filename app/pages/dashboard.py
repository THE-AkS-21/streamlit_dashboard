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

CHART_TYPES = ["Line", "Bar", "Area", "Scatter", "Pie", "Box", "Histogram", "Sunburst", "Histogram+Area", "Selected Time Series"]

@st.cache_data(ttl=3600, show_spinner="🔄 Loading filter metadata...")
def get_dashboard_metadata():
    loader = show_loader("Loading filter metadata...")
    data = db.execute_query(DashboardQueries.GET_DASHBOARD_FILTER_METADATA)
    loader.empty()
    return data

@st.cache_data(ttl=3600)
def get_all_data(start_date, end_date):
    return db.execute_query(
        DashboardQueries.GET_DASHBOARD_CHART_DATA,
        {"start_date": start_date, "end_date": end_date}
    )

def render_filter_form(metadata_df):
    categories = sorted(filter(None, metadata_df['category'].unique()))
    subcategories = sorted(filter(None, metadata_df['subcategory'].unique()))
    skus = sorted(filter(None, metadata_df['sku'].unique()))
    last_date = metadata_df['last_date'].max()

    with st.form(key="dashboard_form"):
        col1, col2, col3, col4, col5 = st.columns([1.5, 1.5, 2, 1.5, 1.5], gap="small")

        category = col1.selectbox("Category", ["None"] + categories)
        subcategory = col2.selectbox("Subcategory", ["None"] + subcategories)
        sku = col3.selectbox("SKU", ["None"] + skus)
        start_date = col4.date_input("Start Date", value=datetime(2024, 6, 1))
        end_date = col5.date_input("End Date", value=last_date)

        action_col1, action_col2, action_col3 = st.columns([2, 1, 1])
        plot_button = action_col1.form_submit_button("Generate Report", use_container_width=True)
        fetch_button = action_col2.form_submit_button("Fetch", use_container_width=True)
        edit_button = action_col3.form_submit_button("Edit Orders", use_container_width=True)

    return category, subcategory, sku, start_date, end_date, plot_button, fetch_button, edit_button

def run_dashboard_query(sku, start_date, end_date):
    query = DashboardQueries.MONTHLY_ORDERS_WITH_SKU if sku != "None" else DashboardQueries.MONTHLY_ORDERS_NO_SKU
    params = {"start_date": start_date, "end_date": end_date}
    if sku != "None":
        params["whsku"] = sku
    return query, params, db.execute_query(query, params)

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
                    default=[],
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

                if chart_type in ["Histogram+Area", "Selected Time Series"]:
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
    st.markdown("## Bombay Shaving Company Dashboard")

    st.session_state.setdefault("report_tabs", [])
    st.session_state.setdefault("report_data", {})
    st.session_state.setdefault("last_query", None)

    metadata_df = get_dashboard_metadata()
    category, subcategory, sku, start_date, end_date, plot_btn, fetch_btn, edit_btn = render_filter_form(metadata_df)

    if fetch_btn:
        st.cache_data.clear()
        query, params, refreshed_df = run_dashboard_query(sku, start_date, end_date)

        if not refreshed_df.empty:
            if st.session_state["last_query"]:
                for tab in st.session_state.report_tabs:
                    st.session_state.report_data[tab] = refreshed_df
                st.success("✅ Data refreshed for all reports.")
            else:
                st.success("✅ Data fetched. No reports yet.")
            st.rerun()
        else:
            st.error("❌ No data found for the current filters.")

    if plot_btn:
        query, params, orders_df = run_dashboard_query(sku, start_date, end_date)

        if not orders_df.empty:
            tab_name = f"{sku if sku != 'None' else 'All SKUs'} | {start_date} → {end_date} | #{len(st.session_state.report_tabs) + 1}"
            st.session_state.report_tabs.append(tab_name)
            st.session_state.report_data[tab_name] = orders_df
            st.session_state["last_query"] = (query, params)
            st.rerun()
        else:
            st.error("❌ No data found to generate report.")

    if st.session_state.report_tabs:
        render_report_tabs(start_date, end_date)

    if edit_btn:
        _, _, orders_df = run_dashboard_query(sku, start_date, end_date)

        if not orders_df.empty:
            st.markdown("### Edit Orders Data")
            edited_df = st.data_editor(orders_df, num_rows="dynamic", use_container_width=True)

            if st.button("Save Changes", use_container_width=True):
                try:
                    for _, row in edited_df.iterrows():
                        db.execute_query(
                            DashboardQueries.UPDATE_ORDER_VALUE,
                            {
                                "orderdate": row["time"],
                                "whsku": sku if sku != "None" else row.get("sku"),
                                "value": row["value"],
                            }
                        )
                    st.success("✅ Changes saved successfully!")
                except Exception as e:
                    st.error(f"❌ Error saving changes: `{str(e)}`")

    if not any([fetch_btn, plot_btn, edit_btn]):
        st.info("""
            👋 **Welcome to the BSC Orders Dashboard!**
            - Select filters  
            - Click **Fetch**, **Generate Report**, or **Edit Orders**
        """)
