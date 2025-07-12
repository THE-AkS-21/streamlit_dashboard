from datetime import datetime
import streamlit as st
from app.components.content_area import render_content_end, render_content_start
from app.database.connection import db
from app.database.queries.dashboard_queries import DashboardQueries
from app.components.charts import ChartComponent
from app.utils.formatters import Formatters

@st.cache_data(ttl=3600, show_spinner="🔄 Loading filter metadata...")
def get_dashboard_metadata():
    return db.execute_query(DashboardQueries.GET_DASHBOARD_FILTER_METADATA)

def show_dashboard():
    render_content_start()
    st.markdown("## Bombay Shaving Company Dashboard")
    st.markdown("""
        <style>
        .form-container {
            background-color: #F9FAFB;
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #E5E7EB;
            margin-bottom: 30px;
        }
        .metric-card {
            background-color: #FFFFFF;
            padding: 18px;
            border-radius: 12px;
            border: 1px solid #E5E7EB;
            text-align: center;
        }
        .metric-label {
            font-size: 0.9rem;
            color: #6B7280;
            margin-bottom: 5px;
        }
        .metric-value {
            font-size: 1.7rem;
            font-weight: 600;
            color: #111827;
        }
        </style>
    """, unsafe_allow_html=True)

    metadata_df = get_dashboard_metadata()

    categories = sorted([c for c in metadata_df['category'].unique() if c is not None])
    subcategories = sorted([sc for sc in metadata_df['subcategory'].unique() if sc is not None])
    skus = sorted([s for s in metadata_df['sku'].unique() if s is not None])
    last_date = metadata_df['last_date'].max()  # or .iloc[0] as it's same value repeated

    with st.container():
        with st.form(key='chart_form'):
            st.markdown("### Filter Parameters")

            col1, col2, col3, col4, col5 = st.columns([1.5, 1.5, 2, 1.5, 1.5])

            with col1:
                category = st.selectbox("Category", categories)

            with col2:
                subcategory = st.selectbox("Subcategory", subcategories)

            with col3:
                sku = st.selectbox("SKU", skus)

            with col4:
                start_date = st.date_input("Start Date", value=datetime(2024, 6, 1))

            with col5:
                end_date = st.date_input("End Date", value=last_date)

            st.markdown("<br>", unsafe_allow_html=True)

            action_col1, action_col2 = st.columns([2, 1])

            with action_col1:
                plot_button = st.form_submit_button(
                    label="Generate Report",
                    type="primary",
                    use_container_width=True
                )

            with action_col2:
                if st.form_submit_button("Fetch", use_container_width=True):
                    st.cache_data.clear()
                    st.cache_resource.clear()


    if plot_button:
        try:
            with st.spinner('📡 Fetching and processing data...'):
                orders_df = db.execute_query(
                    DashboardQueries.MONTHLY_ORDERS,
                    {'whsku': sku, 'start_date': start_date, 'end_date': end_date}
                )

                if orders_df.empty:
                    st.warning("⚠️ No data found for the selected criteria.")
                else:
                    st.markdown("### Dashboard Metrics")

                    col1, col2, col3 = st.columns(3)
                    metrics = [
                        {'label': 'Total Units', 'value': Formatters.number(orders_df['value'].sum())},
                        {'label': 'Average Daily Units', 'value': Formatters.number(orders_df['value'].mean())},
                        {'label': 'Days with Orders', 'value': Formatters.number(len(orders_df))}
                    ]

                    for i, col in enumerate([col1, col2, col3]):
                        with col:
                            st.markdown(f"""
                                <div class="metric-card">
                                    <div class="metric-label">{metrics[i]['label']}</div>
                                    <div class="metric-value">{metrics[i]['value']}</div>
                                </div>
                            """, unsafe_allow_html=True)

                    st.markdown(f"### Daily Orders Trend for **{sku}**")

                    tab1, tab2 = st.tabs(["Interactive Chart", "Raw Data"])

                    with tab1:
                        ChartComponent.orders_chart(orders_df, key=f"{sku}_{start_date}_{end_date}")

                        st.caption("""
                        💡 **Chart Tips:**
                        - Hover over points for exact values
                        - Click & drag to zoom
                        - Double-click to reset view
                        - Use mouse wheel to scroll through time
                        """)

                    with tab2:
                        display_df = orders_df.copy()
                        display_df.columns = ['Date', 'Units']
                        st.dataframe(display_df.style.format({'Units': '{:,.0f}'}), use_container_width=True)

                    st.download_button(
                        label="📥 Download CSV Report",
                        data=orders_df.to_csv(index=False),
                        file_name=f'orders_data_{sku}_{start_date}_{end_date}.csv',
                        mime='text/csv',
                        use_container_width=True
                    )

        except Exception as e:
            st.error(f"❌ Error loading dashboard data: `{str(e)}`")

    else:
        st.info("""
        👋 **Welcome to the BSC Orders Dashboard!**

        To get started:
        1. Select your SKU
        2. Pick a date range
        3. Click **Plot Data** to visualize
        """)
    render_content_end()