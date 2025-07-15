import streamlit as st
from datetime import date
from app.database.connection import db
from app.database.queries.sku_analytics_queries import SkuAnalyticsQueries
from app.utils.global_css import apply_global_styles
from app.components.aggrid_renderer import render_aggrid

def show_sku_analytics():
    apply_global_styles()

    st.markdown('<h2 class="page-title">SKU Channel Analytics</h2>', unsafe_allow_html=True)

    # Unified filters + fetch button row
    col1, col2, col3, col4, col5 = st.columns([1.5, 1.5, 1, 1, 0.7])

    with col1:
        start_date = st.date_input("Start Date", value=date(2025, 1, 1))

    with col2:
        end_date = st.date_input("End Date", value=date(2025, 4, 1))

    with col3:
        limit = st.selectbox("Rows per Page", [5, 20, 30, 50], index=1)

    with col4:
        page_no = st.number_input("Page No", min_value=1, value=1, step=1)

    with col5:
        st.markdown("""<div style="margin-top: 20px;"></div>""", unsafe_allow_html=True)
        fetch_button = st.button("🔄 Fetch", key="fetch_btn", help="Clear cache & fetch fresh data")

    # Validate date input
    if start_date > end_date:
        st.error("❌ Start date cannot be after end date.")
        return

    # Handle fetch button click to clear cache if applicable
    if fetch_button:
        st.cache_data.clear()  # or your caching mechanism

    # Always fetch and render data (either cached or fresh after button click)
    params = {
        "start_date": start_date,
        "end_date": end_date,
        "limit": limit,
        "page_no": page_no
    }

    query = SkuAnalyticsQueries.FETCH_SKU_CHANNEL_PNL_PAGINATION
    data_df = db.execute_query(query, params)

    st.markdown('<div class="analytics-container" style="margin-top: 16px;">', unsafe_allow_html=True)

    if data_df.empty:
        st.warning("⚠️ No records found for the selected range and page.")
    else:
        render_aggrid(data_df, page_size=limit)

    st.markdown('</div>', unsafe_allow_html=True)
