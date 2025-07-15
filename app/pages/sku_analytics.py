import streamlit as st
from datetime import date
from app.database.connection import db
from app.database.queries.sku_analytics_queries import SkuAnalyticsQueries
from app.utils.global_css import apply_global_styles

def show_sku_analytics():
    apply_global_styles()

    # Page title
    st.markdown('<h2 class="page-title">SKU Channel Analytics</h2>', unsafe_allow_html=True)

    # ───── Date filters ─────
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=date(2025, 1, 1))
    with col2:
        end_date = st.date_input("End Date", value=date(2025, 4, 1))

    if start_date > end_date:
        st.error("❌ Start date cannot be after end date.")
        return

    # ───── Pagination controls ─────
    col3, col4 = st.columns(2)
    with col3:
        limit = st.selectbox("Rows per Page", [5, 20, 30, 50], index=1)
    with col4:
        page_no = st.number_input("Page No", min_value=1, value=1, step=1)

    # ───── Data Fetch ─────
    params = {
        "start_date": start_date,
        "end_date": end_date,
        "limit": limit,
        "page_no": page_no
    }

    query = SkuAnalyticsQueries.FETCH_SKU_CHANNEL_PNL_PAGINATION
    data_df = db.execute_query(query, params)

    if data_df.empty:
        st.warning("⚠️ No records found for the selected range and page.")
        return

    # ───── Data Table Display ─────
    st.markdown('<div class="analytics-container">', unsafe_allow_html=True)

    # Optional: Style it centrally if needed (already styled via CSS, but you can also do it in Python)
    styled_df = data_df.style.set_properties(
        **{
            "text-align": "center"
        }
    )

    st.data_editor(
        data_df,
        hide_index=True,
        use_container_width=True,
        column_config={col: {"width": "160px"} for col in data_df.columns},
        key=f"editor_{page_no}"
    )

    st.markdown('</div>', unsafe_allow_html=True)
