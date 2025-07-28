import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid import GridUpdateMode
from st_aggrid.shared import JsCode

# Load AG Grid license key from secrets (ensure it's valid!)
license_Key = st.secrets["AG_GRID_LICENSE"]["key"]

def render_aggrid(data_df: pd.DataFrame):
    data_df = data_df.copy()
    page_size = 50

    # ───── Configure AG Grid ─────

    #  Custom cellStyle
    cm2_percentage_style = JsCode("""
                        function(params) {
                            const val = params.value;
                            if (val >= 25) {
                                return { fontWeight: 'bold', color: '#006400' }; // Dark Green
                            } else if (val >= 20) {
                                return { fontWeight: 'bold', color: '#228B22' }; // Forest Green
                            } else if (val >= 15) {
                                return { fontWeight: 'bold', color: '#32CD32' }; // Lime Green
                            } else if (val >= 10) {
                                return { fontWeight: 'bold', color: '#FFA500' }; // Orange
                            } else if (val >= 5) {
                                return { fontWeight: 'bold', color: '#FF4C4C' }; // Red
                            } else {
                                return { fontWeight: 'bold', color: '#8B0000' }; // Deep Dark Red
                            }
                        }
                        """)

    cm2_trend_renderer = JsCode("""
                        function(params) {
                            const val = params.value;
                            if (val >= 25) {
                                return '★ ' + val + '%';
                            } else if(val>=20){
                                return '⬆ ' + val + '%';
                            }else if (val >= 15) {
                                return '↗ ' + val + '%';
                            } else if (val >= 10) {
                                return '➡ ' + val + '%';
                            } else if (val >= 5) {
                                return '↘ ' + val + '%';
                            } else {
                                return '⬇ ' + val + '%';
                            }
                        }
                        """)

    cm1_percentage_style = JsCode("""
                            function(params) {
                                const val = params.value;
                                if (val >= 50) {
                                    return { fontWeight: 'bold', color: '#006400' }; // Dark Green
                                } else if (val >= 45) {
                                    return { fontWeight: 'bold', color: '#228B22' }; // Forest Green
                                } else if (val >= 40) {
                                    return { fontWeight: 'bold', color: '#32CD32' }; // Lime Green
                                } else if (val >= 35) {
                                    return { fontWeight: 'bold', color: '#FFA500' }; // Orange
                                } else if (val >= 30) {
                                    return { fontWeight: 'bold', color: '#FF4C4C' }; // Red
                                } else {
                                    return { fontWeight: 'bold', color: '#8B0000' }; // Deep Dark Red
                                }
                            }
                            """)

    cm1_trend_renderer = JsCode("""
                            function(params) {
                                const val = params.value;
                                if (val >= 50) {
                                    return '★ ' + val + '%';
                                } else if(val>=45){
                                    return '⬆ ' + val + '%';
                                }else if (val >= 40) {
                                    return '↗ ' + val + '%';
                                } else if (val >= 35) {
                                    return '➡ ' + val + '%';
                                } else if (val > 25) {
                                    return '↘ ' + val + '%';
                                } else {
                                    return '⬇ ' + val + '%';
                                }
                            }
                            """)

    gmgp_percentage_style = JsCode("""
                            function(params) {
                                const val = params.value;
                                if (val >= 55) {
                                    return { fontWeight: 'bold', color: '#006400' }; // Dark Green
                                } else if (val >= 50) {
                                    return { fontWeight: 'bold', color: '#228B22' }; // Forest Green
                                } else if (val >= 45) {
                                    return { fontWeight: 'bold', color: '#32CD32' }; // Lime Green
                                } else if (val >= 40) {
                                    return { fontWeight: 'bold', color: '#FFA500' }; // Orange
                                } else if (val >= 35) {
                                    return { fontWeight: 'bold', color: '#FF4C4C' }; // Red
                                } else {
                                    return { fontWeight: 'bold', color: '#8B0000' }; // Deep Dark Red
                                }
                            }
                            """)

    gmgp_trend_renderer = JsCode("""
                            function(params) {
                                const val = params.value;
                                if (val >= 55) {
                                    return '★ ' + val + '%';
                                } else if(val>=50){
                                    return '⬆ ' + val + '%';
                                }else if (val >= 45) {
                                    return '↗ ' + val + '%';
                                } else if (val >= 40) {
                                    return '➡ ' + val + '%';
                                } else if (val > 30) {
                                    return '↘ ' + val + '%';
                                } else {
                                    return '⬇ ' + val + '%';
                                }
                            }
                            """)

    gb = GridOptionsBuilder.from_dataframe(data_df)

    for col in data_df.columns:
        # Dynamically format header name
        if col.lower().endswith("percentage"):
            header_name = col[:-10].replace("_", " ").title() + " %"
        else:
            header_name = col.replace("_", " ").title()

        gb.configure_column(
            col,
            headerName=header_name,
            filter=True,
            sortable=True,
            resizable=True,
            editable=False,
            minWidth=120
        )
    # Basic column settings
    # ───── Basic Features ─────
    gb.configure_default_column(
        editable=True,
        groupable=True,
        value=True,
        enableRowGroup=True,
        enablePivot=False,
        enableValue=True,
        sortable=True,
        resizable=True,
        filter=True,
        checkboxSelection=False,
        suppressMenu=False,
    )
    # ───── Enterprise Features ─────
    gb.configure_grid_options(
        rowGroupPanelShow='always',  # Enables row grouping panel
        pivotPanelShow='always',  # Enables pivot panel
        enableRangeSelection=True,  # ⚠️ Deprecated in v32. Use cellSelection instead
        cellSelection=True,  # ✅ New way to allow range selection
        enableCharts=True,  # Enables charting
        animateRows=True,  # Smooth row animations
        suppressAggFuncInHeader=True,  # Clean header when grouped
        pagination=True,  # Enable pagination
        paginationAutoPageSize=False,
        paginationPageSize=page_size,
        suppressRowClickSelection=False,
        rowSelection="multiple",  # 'single' or 'multiple'
        sideBar=True,  # Shows sidebar with filters, columns
        pivotMode=True,  # Allow pivoting
    )

    # Pagination
    # gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=50)

    # Enable Cell Styling
    gb.configure_column("cm2percentage", headerName="CM2 %", cellStyle=cm2_percentage_style, pinned="left",
                        cellRenderer=cm2_trend_renderer)
    gb.configure_column("cm1percentage", headerName="CM1 %", cellStyle=cm1_percentage_style, pinned="left",
                        cellRenderer=cm1_trend_renderer)
    gb.configure_column("gmgppercentage", headerName="GMGP %", cellStyle=gmgp_percentage_style, pinned="left",
                        cellRenderer=gmgp_trend_renderer)
    gb.configure_column("valuationdate", pinned="left", headerClass="ag-header-bold")
    grid_options = gb.build()

    # Render grid
    grid_response = AgGrid(
        data_df,
        gridOptions=grid_options,
        # theme="alpine",
        update_mode=GridUpdateMode.MODEL_CHANGED,
        data_return_mode="AS_INPUT",
        fit_columns_on_grid_load=True,
        allow_unsafe_jscode=True,  # Allow JS customization
        enable_enterprise_modules=True,  # 🟢 Enables enterprise features
        height=600,
        width='100%',
        reload_data=False,
    )

    return grid_response