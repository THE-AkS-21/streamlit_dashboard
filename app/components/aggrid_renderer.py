import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd

def render_aggrid(data_df, page_size=20):
    st.markdown("""
        <style>
        .ag-theme-alpine .ag-header-cell, 
        .ag-theme-alpine .ag-cell {
            text-align: center;
        }
        .ag-theme-alpine .ag-header-cell-label {
            justify-content: center;
        }
        </style>
    """, unsafe_allow_html=True)

    # Add Serial Number Column
    data_df.insert(0, "S.No", range(1, len(data_df) + 1))

    gb = GridOptionsBuilder.from_dataframe(data_df)

    for col in data_df.columns:
        gb.configure_column(
            col,
            headerName=col,
            filter=True,
            sortable=True,
            resizable=True,
            minWidth=120
        )

    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=page_size)
    gb.configure_grid_options(domLayout='normal')

    AgGrid(
        data_df,
        gridOptions=gb.build(),
        theme="alpine",
        height=600,
        enable_enterprise_modules=True,
        allow_unsafe_jscode=True,
        fit_columns_on_grid_load=True
    )
