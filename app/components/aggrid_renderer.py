import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder


def render_aggrid(data_df: pd.DataFrame):
    data_df = data_df.copy()
    page_size = 50

    # ───── Add Serial Number ─────
    if "S.No" not in data_df.columns:
        data_df.insert(0, "S.No", range(1, len(data_df) + 1))

    # ───── Configure AG Grid ─────
    gb = GridOptionsBuilder.from_dataframe(data_df)

    for col in data_df.columns:
        gb.configure_column(
            col,
            headerName=col,
            filter=True,
            sortable=True,
            resizable=True,
            editable=False,
            minWidth=120
        )

    # ✅ Enable Sidebar (columns & filters)
    gb.configure_side_bar()
    # ✅ Enable Sidebar (row grouping)
    gb.configure_default_column(groupable=True)
    gb.configure_grid_options(floatingFilter=True)
    # ✅ Enable Row Selection
    gb.configure_selection("multiple", use_checkbox=True)
    # ✅ Enable Pagination
    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=page_size)

    # ───── Render AG Grid ─────
    grid_response = AgGrid(
        data_df,
        gridOptions=gb.build(),
        theme="alpine",
        height=600,
        allow_unsafe_jscode=True,
        enable_enterprise_modules=True,
        fit_columns_on_grid_load=False,
    )
