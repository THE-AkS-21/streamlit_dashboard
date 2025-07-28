import streamlit as st
from datetime import date
import time

from app.database.connection import db
from app.database.queries.sku_analytics_queries import SkuAnalyticsQueries
from app.utils.global_css import apply_global_styles
from app.components.aggrid_renderer import render_aggrid
from app.components.export_controls import export_controls


@st.cache_data(ttl=3600)
def get_cached_sku_data(start_date, end_date, limit, page_no):
    params = {
        "start_date": start_date,
        "end_date": end_date,
        "limit": limit,
        "page_no": page_no
    }
    query = SkuAnalyticsQueries.FETCH_SKU_CHANNEL_PNL_PAGINATION
    return db.execute_query(query, params)


def show_sku_analytics():
    apply_global_styles()
    st.markdown('<h2 class="page-title">SKU Channel Analytics</h2>', unsafe_allow_html=True)

    # ───── Filter + Export Layout ─────
    with st.container():
        col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 1, 0.7, 0.7, 1, 1.2, 1])

        with col1:
            start_date = st.date_input("Start Date", value=date(2025, 1, 1))

        with col2:
            end_date = st.date_input("End Date", value=date(2025, 4, 1))

        with col3:
            limit = st.number_input("Rows per Page", min_value=1, value=50, step=1)

        with col4:
            page_no = st.number_input("Page No", min_value=1, value=1, step=1)

        with col5:
            export_type = st.selectbox(
                "Export As",
                options=["None", "CSV", "Excel", "PDF", "PNG"],
                key="export_type_dropdown"
            )

        with col6:
            st.markdown("""<div style="margin-top: 10px;"></div>""", unsafe_allow_html=True)
            export_btn = st.button("Download", key="download_btn", help="Export file")

        with col7:
            st.markdown("""<div style="margin-top: 10px;"></div>""", unsafe_allow_html=True)
            fetch_button = st.button("Fetch", key="fetch_btn", help="Reload data without cache")

    # ───── Validate Dates ─────
    if start_date > end_date:
        st.error("❌ Start date cannot be after end date.")
        return

    # ───── Fetch Data ─────
    if fetch_button:
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "limit": limit,
            "page_no": page_no
        }
        start_time = time.time()
        query = SkuAnalyticsQueries.FETCH_SKU_CHANNEL_PNL_PAGINATION
        data_df = db.execute_query(query, params)
        duration = time.time() - start_time
        st.success(f"✅ Data fetched in {duration:.2f} seconds")
    else:
        data_df = get_cached_sku_data(start_date, end_date, limit, page_no)

    # ───── Export on Button Click ─────
    if export_btn and export_type != "None" and not data_df.empty:
        filename, content, mime, download_html = export_controls(
            data_df,
            file_prefix="sku_analytics_export",
            export_type=export_type
        )
        if export_type != "PNG":
            st.download_button(
                label=f"Download {export_type}",
                data=content,
                file_name=filename,
                mime=mime,
                use_container_width=True
            )
        else:
            st.markdown(download_html, unsafe_allow_html=True)

    # ───── Render Grid ─────
    st.markdown('<div class="analytics-container">', unsafe_allow_html=True)

    if data_df.empty:
        st.warning("⚠️ No records found for the selected range and page.")
    else:
        render_aggrid(data_df)

    st.markdown('</div>', unsafe_allow_html=True)
