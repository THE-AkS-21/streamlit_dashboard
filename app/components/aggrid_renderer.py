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

    # ───── Extract Visible Columns ─────
    column_state = grid_response.get("column_state", [])
    visible_columns = set()

    if column_state:
        for col in column_state:
            col_id = col.get("colId")
            if col_id and not col.get("hide", False):
                visible_columns.add(col_id)

    # Fallback to all columns if none are marked visible
    if not visible_columns:
        visible_columns = set(data_df.columns)

    # ───── Prepare Selected Column Data ─────
    selected_column_data = {
        col: data_df[col].tolist()
        for col in visible_columns if col in data_df.columns
    }

    selected_rows_df = pd.DataFrame(grid_response["selected_rows"]) if grid_response[
        "selected_rows"] else pd.DataFrame()

    # ✅ This will actually print the data for each selected column
    # Example: {'netsales': [123, 456, ...], 'discountactual': [12, 15, ...], ...}
    print("Selected Column Data (with values):")
    for col, values in selected_column_data.items():
        print(f"{col}: {values[:5]}...")  # Only printing first 5 values for readability

    return {
        "full_data": data_df,
        "selected_rows": selected_rows_df,
        "selected_column_data": selected_column_data
    }
