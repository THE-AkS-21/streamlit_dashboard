from datetime import datetime
import streamlit as st
import pandas as pd

from app.components.aggrid_renderer import render_aggrid
from app.database.connection import db
from app.database.queries.dashboard_queries import DashboardQueries
from app.components.charts import ChartComponent
from app.utils.formatters import Formatters
from app.utils.global_css import apply_global_styles

@st.cache_data(ttl=3600, show_spinner="🔄 Loading filter metadata...")
def get_dashboard_metadata():
    return db.execute_query(DashboardQueries.GET_DASHBOARD_FILTER_METADATA)

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
            # ─── Header and Close Button ───
            col1, col2 = st.columns([10, 1])
            with col1:
                st.markdown(f"### {tab_name}")
            with col2:
                if st.button("❌", key=f"close_{tab_name}", use_container_width=True):
                    st.session_state.report_tabs.remove(tab_name)
                    st.session_state.report_data.pop(tab_name)
                    st.rerun()

            # ─── Ensure 'value' Column ───
            if "value" not in orders_df.columns:
                orders_df["value"] = orders_df.get("units", 0)

            # ─── Metric Cards ───
            ChartComponent.metric_cards([
                {"label": "Total Units", "value": Formatters.number(orders_df["value"].sum())},
                {"label": "Avg Daily Units", "value": Formatters.number(orders_df["value"].mean())},
                {"label": "Days", "value": Formatters.number(len(orders_df))},
            ]
            ChartComponent.metric_cards(metrics)

            st.markdown("#### Ag-Grid")

            data_df = get_all_data(start_date, end_date)

            if data_df.empty:
                st.warning("⚠️ No records found for the selected range and page.")
            else:
                render_aggrid(data_df)

            st.markdown("#### Chart")

            chart_type = st.selectbox(
                "Select Chart Type",
                ["Histogram+Area","Line", "Bar", "Area", "Scatter", "Pie", "Box", "Histogram", "Sunburst"],
                key=f"{tab_name}_chart_type"
            )
            df = orders_df.copy()

            # Coerce datetime and numeric values
            if "time" in df.columns:
                df["time"] = pd.to_datetime(df["time"], errors="coerce")
            if "value" in df.columns:
                df["value"] = pd.to_numeric(df["value"], errors="coerce")

            df = df.dropna(subset=["time", "value"])

            if df.empty:
                st.warning("No valid data available for chart.")
            else:
                chart_component = ChartComponent(df)

                if chart_type == "Histogram+Area":
                    chart_component.asp_units_offtake_chart()
                else:
                    chart_component.render_dynamic_chart(
                        x_axis="time",
                        y_axis="value",
                        chart_type=chart_type
                    )

                # ─── Download CSV ───
                st.download_button(
                    label="📥 Download CSV Report",
                    data=df.to_csv(index=False),
                    file_name=f"{tab_name}_{selected_column}_chart.csv",
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
