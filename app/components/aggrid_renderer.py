import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from app.components.export_controls import export_controls


def render_aggrid(data_df: pd.DataFrame, page_size: int = 50):
    data_df = data_df.copy()

    # Add Serial Number column
    if "S.No" not in data_df.columns:
        data_df.insert(0, "S.No", range(1, len(data_df) + 1))

    all_columns = list(data_df.columns)
    visible_columns = [col for col in all_columns if col != "S.No"]

    # Set session defaults
    st.session_state.setdefault("selected_columns", visible_columns)
    st.session_state.setdefault("dropdown_open", False)

    # ───── UI: Filter + Export ─────
    st.markdown('<div class="filter-export-container">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([3, 1.5, 1])

    with col1:
        if st.button("📊 Select Columns ▼", key="dropdown_toggle_btn", use_container_width=True):
            st.session_state.dropdown_open = not st.session_state.dropdown_open

        # Toggle dropdown visibility using custom CSS class
        dropdown_class = "dropdown-box open" if st.session_state.dropdown_open else "dropdown-box closed"
        st.markdown(f'<div class="{dropdown_class}">', unsafe_allow_html=True)

        # Select All logic
        select_all_state = set(st.session_state.selected_columns) == set(visible_columns)
        select_all = st.checkbox("✅ Select All Columns", value=select_all_state, key="select_all_inside")

        if select_all:
            st.session_state.selected_columns = visible_columns.copy()
        else:
            search_term = st.text_input("🔍 Search Columns", key="search_column_input", label_visibility="collapsed")
            filtered_cols = [col for col in visible_columns if search_term.lower() in col.lower()]

            for col in filtered_cols:
                is_checked = col in st.session_state.selected_columns
                checked = st.checkbox(col, value=is_checked, key=f"checkbox_{col}")
                if checked and col not in st.session_state.selected_columns:
                    st.session_state.selected_columns.append(col)
                elif not checked and col in st.session_state.selected_columns:
                    st.session_state.selected_columns.remove(col)

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        export_format = st.selectbox(
            "📤 Export Format",
            ["CSV", "Excel", "PDF", "PNG"],
            key="export_format_dropdown"
        )

    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Export", use_container_width=True):
            filtered_df = data_df[["S.No"] + st.session_state.selected_columns]
            export_controls(filtered_df, file_prefix="sku_analytics_export", export_type=export_format)

    st.markdown('</div>', unsafe_allow_html=True)

    # ───── Validation ─────
    if not st.session_state.selected_columns:
        st.warning("⚠️ Please select at least one column.")
        return

    # ───── AG Grid Setup ─────
    filtered_df = data_df[["S.No"] + st.session_state.selected_columns]
    gb = GridOptionsBuilder.from_dataframe(filtered_df)
    for col in filtered_df.columns:
        gb.configure_column(col, headerName=col, filter=True, sortable=True, resizable=True, minWidth=120)

    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=page_size)
    gb.configure_grid_options(domLayout="normal")

    AgGrid(
        filtered_df,
        gridOptions=gb.build(),
        theme="alpine",
        height=600,
        enable_enterprise_modules=True,
        allow_unsafe_jscode=True,
        fit_columns_on_grid_load=True
    )
