# app/components/filters.py

import streamlit as st
from app.database.connection import db


def render_global_filters():
    st.sidebar.header("🔍 Global Filters")

    # Query distinct values for each filter
    category_options = fetch_filter_values("category")
    subcategory_options = fetch_filter_values("subcategory")
    sku_options = fetch_filter_values("whsku")

    # Date range filter (valuationdate)
    date_range = st.sidebar.date_input(
        "📅 Valuation Date Range",
        value=(None, None),
        help="Filter by valuation date range"
    )

    selected_categories = st.sidebar.multiselect("🗂️ Category", category_options)
    selected_subcategories = st.sidebar.multiselect("📂 Subcategory", subcategory_options)
    selected_skus = st.sidebar.multiselect("🔢 SKU (whsku)", sku_options)

    # Build WHERE clauses
    filters = {
        "category": f"AND category IN :category" if selected_categories else "",
        "subcategory": f"AND subcategory IN :subcategory" if selected_subcategories else "",
        "whsku": f"AND whsku IN :whsku" if selected_skus else "",
        "valuationdate": ""
    }

    if date_range and all(date_range):
        filters["valuationdate"] = "AND valuationdate BETWEEN :start_date AND :end_date"

    return filters, {
        "category": selected_categories,
        "subcategory": selected_subcategories,
        "whsku": selected_skus,
        "start_date": str(date_range[0]) if date_range and all(date_range) else None,
        "end_date": str(date_range[1]) if date_range and all(date_range) else None,
    }


def fetch_filter_values(column: str):
    query = f"SELECT DISTINCT {column} FROM orders ORDER BY {column}"
    df = db.execute_query(query)
    return df[column].dropna().tolist()
