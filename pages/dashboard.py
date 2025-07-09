from datetime import datetime
import streamlit as st
from app.database.connection import db
from app.database.queries.dashboard_queries import DashboardQueries
from app.components.charts import ChartComponent
from app.utils.formatters import Formatters

def show_dashboard():
    st.title("BSC Orders Dashboard")

    with st.form(key='chart_form'):
        sku = st.selectbox(
            "Select SKU",
            ["SHAVE_SENSITIVE_FOAM_264G"],
            index=0
        )

        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", value=datetime(2024, 6, 1))
        with col2:
            end_date = st.date_input("End Date", value=datetime(2024, 6, 26))

        plot_button = st.form_submit_button(
            label="Plot Data",
            type="primary",
            use_container_width=True
        )

    if plot_button:
        try:
            with st.spinner('Fetching and processing data...'):
                orders_df = db.execute_query(
                    DashboardQueries.MONTHLY_ORDERS,
                    {
                        'whsku': sku,
                        'start_date': start_date,
                        'end_date': end_date
                    }
                )

                if orders_df.empty:
                    st.warning("No data found for the selected criteria.")
                else:
                    metrics = [
                        {
                            'label': 'Total Units',
                            'value': Formatters.number(orders_df['value'].sum())
                        },
                        {
                            'label': 'Average Daily Units',
                            'value': Formatters.number(orders_df['value'].mean())
                        },
                        {
                            'label': 'Days with Orders',
                            'value': Formatters.number(len(orders_df))
                        }
                    ]

                    st.subheader("📊 Dashboard Metrics")
                    ChartComponent.metric_cards(metrics)

                    st.subheader(f"📈 Daily Orders Trend for {sku}")

                    tab1, tab2 = st.tabs(["Interactive Chart", "Raw Data"])

                    with tab1:
                        ChartComponent.orders_chart(orders_df, key=f"{sku}_{start_date}_{end_date}")

                        st.caption("""
                        💡 **Chart Tips:**
                        - Hover over the chart to see exact values
                        - Click and drag to zoom
                        - Double-click to reset zoom
                        - Use mouse wheel to scroll through time
                        """)

                    with tab2:
                        display_df = orders_df.copy()
                        display_df.columns = ['Date', 'Units']
                        st.dataframe(display_df.style.format({'Units': '{:,.0f}'}), use_container_width=True)

                    csv = orders_df.to_csv(index=False)
                    st.download_button(
                        label="Download Data as CSV",
                        data=csv,
                        file_name=f'orders_data_{sku}_{start_date}_{end_date}.csv',
                        mime='text/csv',
                        use_container_width=True
                    )

        except Exception as e:
            st.error(f"Error loading dashboard data: {str(e)}")

    else:
        st.info("""
        👋 **Welcome to the BSC Orders Dashboard!**

        To get started:
        1. Select your SKU from the dropdown
        2. Choose your date range
        3. Click the "Plot Data" button to generate the visualization
        """)
