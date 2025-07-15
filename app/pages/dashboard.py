from datetime import datetime
import streamlit as st

from app.database.connection import db
from app.database.queries.dashboard_queries import DashboardQueries
from app.components.charts import ChartComponent
from app.utils.formatters import Formatters
from app.utils.global_css import apply_global_styles


@st.cache_data(ttl=3600, show_spinner="🔄 Loading filter metadata...")
def get_dashboard_metadata():
    return db.execute_query(DashboardQueries.GET_DASHBOARD_FILTER_METADATA)


def show_dashboard():
    apply_global_styles()
    st.markdown('<div class="custom-content">', unsafe_allow_html=True)
    st.markdown("## Bombay Shaving Company Dashboard")

    # Initialize session state
    st.session_state.setdefault("report_tabs", [])
    st.session_state.setdefault("report_data", {})
    st.session_state.setdefault("last_query", None)

    metadata_df = get_dashboard_metadata()
    categories = sorted([c for c in metadata_df['category'].unique() if c])
    subcategories = sorted([sc for sc in metadata_df['subcategory'].unique() if sc])
    skus = sorted([s for s in metadata_df['sku'].unique() if s])
    last_date = metadata_df['last_date'].max()

    with st.container():
        with st.form(key="dashboard_form"):
            col1, col2, col3, col4, col5 = st.columns([1.5, 1.5, 2, 1.5, 1.5], gap="small")
            category = col1.selectbox("Category", ["None"] + categories, index=0)
            subcategory = col2.selectbox("Subcategory", ["None"] + subcategories, index=0)
            sku = col3.selectbox("SKU", ["None"] + skus, index=0)
            start_date = col4.date_input("Start Date", value=datetime(2024, 6, 1))
            end_date = col5.date_input("End Date", value=last_date)

            action_col1, action_col2, action_col3 = st.columns([2, 1, 1])
            plot_button = action_col1.form_submit_button("📊 Generate Report", use_container_width=True)
            fetch_button = action_col2.form_submit_button("📡 Fetch", use_container_width=True)
            edit_button = action_col3.form_submit_button("✏️ Edit Orders", use_container_width=True)

    query_params = {"start_date": start_date, "end_date": end_date}
    if sku != "None":
        query_params["whsku"] = sku

    query_to_run = (
        DashboardQueries.MONTHLY_ORDERS_WITH_SKU
        if sku != "None"
        else DashboardQueries.MONTHLY_ORDERS_NO_SKU
    )

    def run_query_and_get_data():
        data_df = db.execute_query(query_to_run, query_params)
        return data_df if not data_df.empty else None

    # ───── Fetch button logic with banner ─────
    if fetch_button:
        st.cache_data.clear()

        if st.session_state.get("last_query"):
            refreshed_df = run_query_and_get_data()
            if refreshed_df is not None:
                for tname in st.session_state.report_tabs:
                    st.session_state.report_data[tname] = refreshed_df
                st.success("✅ Data refreshed successfully for all existing reports.")
                st.rerun()
            else:
                st.error("❌ No data found for the current filters.")
        else:
            refreshed_df = run_query_and_get_data()
            if refreshed_df is not None:
                st.success("✅ Data fetched and cache cleared — no active reports yet.")
            else:
                st.info("ℹ️ Cache cleared — but no data found for the current selection.")

    # ───── Plot button: always create a new tab ─────
    if plot_button:
        orders_df = run_query_and_get_data()
        if orders_df is not None:
            tab_name = f"{sku if sku != 'None' else 'All SKUs'} | {start_date} → {end_date} | #{len(st.session_state.report_tabs)+1}"
            st.session_state.report_tabs.append(tab_name)
            st.session_state.report_data[tab_name] = orders_df
            st.session_state["last_query"] = (query_to_run, query_params)
            st.rerun()  # instant tab creation on click
        else:
            st.error("❌ No data found to generate report.")

    # ───── Active Tabs rendering ─────
    if st.session_state.report_tabs:
        tabs = st.tabs(st.session_state.report_tabs)
        # inside your tabs loop:
        for i, tname in enumerate(st.session_state.report_tabs):
            orders_df = st.session_state.report_data.get(tname)
            if orders_df is None:
                continue

            with tabs[i]:
                # Top header: tab name + close button in one row
                col1, col2 = st.columns([10, 1])
                with col1:
                    st.markdown(f"### 📊 {tname}")
                with col2:
                    if st.button("❌", key=f"close_{tname}", use_container_width=True):
                        st.session_state.report_tabs.remove(tname)
                        st.session_state.report_data.pop(tname)
                        st.rerun()

                # Metrics Row
                col1, col2, col3 = st.columns(3)
                metrics = [
                    {"label": "Total Units", "value": Formatters.number(orders_df['value'].sum())},
                    {"label": "Avg Daily Units", "value": Formatters.number(orders_df['value'].mean())},
                    {"label": "Days", "value": Formatters.number(len(orders_df))},
                ]
                for j, col in enumerate([col1, col2, col3]):
                    with col:
                        st.markdown(f"""
                            <div class="metric-card">
                                <div class="metric-label">{metrics[j]['label']}</div>
                                <div class="metric-value">{metrics[j]['value']}</div>
                            </div>
                        """, unsafe_allow_html=True)

                # Chart + Data Tabs
                chart_tab, data_tab = st.tabs(["📈 Interactive Chart", "📄 Raw Data"])
                with chart_tab:
                    ChartComponent.orders_chart(orders_df, key=f"{tname}_chart")
                    st.caption("""
                        💡 **Chart Tips:**
                        - Hover for values
                        - Click & drag to zoom
                        - Double-click to reset
                        - Scroll to navigate timeline
                    """)
                with data_tab:
                    display_df = orders_df.copy()
                    display_df.columns = ['Date', 'Units']
                    st.dataframe(display_df.style.format({'Units': '{:,.0f}'}), use_container_width=True)

                st.download_button(
                    label="📥 Download CSV Report",
                    data=orders_df.to_csv(index=False),
                    file_name=f"orders_data_{tname}.csv",
                    mime="text/csv",
                    use_container_width=True
                )

    # ───── Edit Orders ─────
    if edit_button:
        orders_df = run_query_and_get_data()
        if orders_df is not None:
            st.markdown("### Edit Orders Data")
            edited_df = st.data_editor(orders_df, num_rows="dynamic", use_container_width=True)
            if st.button("💾 Save Changes", use_container_width=True):
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

    if not any([fetch_button, plot_button, edit_button]):
        st.info("""
            👋 **Welcome to the BSC Orders Dashboard!**
            - Select filters  
            - Click **Fetch**, **Generate Report** or **Edit Orders**
        """)

    st.markdown('</div>', unsafe_allow_html=True)

