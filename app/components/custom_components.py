import streamlit as st
import pandas as pd
from datetime import datetime
from app.components.charts import ChartComponent
from app.utils.formatters import Formatters
from app.utils.loader import show_loader
from streamlit_aggrid_bridge.MyAgGridComponent import render_aggrid, render_chart
from app.database.connection import db

DEFAULT_START_DATE = datetime(2025, 3, 1).date()
DEFAULT_END_DATE = datetime(2025, 4, 1).date()

def get_filtered_data(category, subcategory, sku, start_date, end_date):
    filters = {"start_date": start_date, "end_date": end_date}
    query = """
        SELECT * FROM bsc.centraldsrdumpv2
        WHERE valuationdate BETWEEN :start_date AND :end_date
    """

    if sku != "None":
        query += " AND whsku = :sku"
        filters["sku"] = sku
    elif subcategory != "None":
        query += " AND subcategory = :subcategory"
        filters["subcategory"] = subcategory
    elif category != "None":
        query += " AND category = :category"
        filters["category"] = category

    return db.execute_query(query, filters)

class Render:
    def __init__(self, page_key: str, start_date, end_date):
        self.page_key = page_key # Added page_key to self
        self.df = st.session_state.get(f"{self.page_key}_filtered_data")
        if self.df is None or self.df.empty:
            # Build the key dynamically using the provided dates
            key = f"dashboard_metadata_{start_date}_{end_date}"

            # Check if the key actually exists before trying to access it
            if key in st.session_state:
                st.session_state[f"{self.page_key}_filtered_data"] = st.session_state[key]
            else:
                # Handle the case where the metadata hasn't been loaded yet
                st.warning("Metadata not found. Please ensure data is loaded before rendering.")
                st.session_state[f"{self.page_key}_filtered_data"] = pd.DataFrame()  # Initialize as empty

    def title(self, title):
        st.title(title)

    def filter(self):

        metadata_df = st.session_state[f"{self.page_key}_filtered_data"]

        categories = sorted(metadata_df['category'].dropna().unique())
        subcategories = sorted(metadata_df['subcategory'].dropna().unique())
        skus = sorted(metadata_df['whsku'].dropna().unique())
        max_date = DEFAULT_END_DATE

        # Load session defaults or assign fallbacks
        start_date = st.session_state.get(f"{self.page_key}_filter_start", DEFAULT_START_DATE)
        end_date = st.session_state.get(f"{self.page_key}_filter_end", max_date)

        col1, col2, col3, col4, col5 = st.columns([1.5, 1.5, 2, 1.5, 1.5], gap="small")

        category = col1.selectbox("Category", ["None"] + categories, key=f"{self.page_key}_filter_category")
        subcategory = col2.selectbox("Subcategory", ["None"] + subcategories, key=f"{self.page_key}_filter_subcategory")
        sku = col3.selectbox("SKU", ["None"] + skus, key=f"{self.page_key}_filter_sku")
        col4.date_input("Start Date", value=start_date, key=f"{self.page_key}_filter_start")
        col5.date_input("End Date", value=end_date, key=f"{self.page_key}_filter_end")

        # Read current filter values from session_state
        start_date = st.session_state[f"{self.page_key}_filter_start"]
        end_date = st.session_state[f"{self.page_key}_filter_end"]

        filters = (category, subcategory, sku, start_date, end_date)
        filter_key = f"{category}_{subcategory}_{sku}_{start_date}_{end_date}"

        if st.session_state.get(f"{self.page_key}_last_filter_key") != filter_key:
            df = get_filtered_data(*filters)

            # Clean up date columns
            for col in df.select_dtypes(include=["datetime64[ns]"]).columns:
                df[col] = df[col].dt.date

            st.session_state[f"{self.page_key}_filtered_data"] = df
            st.session_state[f"{self.page_key}_last_filter_key"] = filter_key

    def metric(self):
        df = st.session_state.get(f"{self.page_key}_filtered_data", pd.DataFrame())
        if df.empty:
            st.warning("⚠️ No data to calculate metrics.")
            return

        start_date = st.session_state["filter_start"]
        end_date = st.session_state["filter_end"]
        num_days = (end_date - start_date).days + 1
        ChartComponent.dynamic_metric_cards([
            {"label": "TOTAL UNITS", "value": Formatters.number(df["units"].sum())},
            {"label": "AVERAGE SELLING PRICE", "value": Formatters.number(df["asp"].mean())},
            {"label": "OFFTAKE", "value": Formatters.number(df["offtake"].sum())},
            {"label": "DAYS", "value": Formatters.number(num_days)},
        ])

    def grid_chart(self):
        df = st.session_state.get(f"{self.page_key}_filtered_data", pd.DataFrame())
        if df.empty:
            st.warning("⚠️ No records found.")
            return

        tab1, tab2 = st.tabs(["DATA", "CHART"])

        with tab1:
            with show_loader("Loading data..."):
                render_aggrid(df)

        with tab2:
            self.chart()

    def grid(self):
        df = st.session_state.get(f"{self.page_key}_filtered_data", pd.DataFrame())
        if df.empty:
            st.warning("⚠️ No records found.")
            return

        with show_loader("Loading data..."):
            render_aggrid(df)

    def chart(self):
        df = st.session_state.get(f"{self.page_key}_filtered_data", pd.DataFrame())
        if df.empty:
            st.warning("⚠️ No records to chart.")
            return

        # numeric_columns = [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col])]
        # col_a, col_b, col_c = st.columns([3, 2, 3])
        #
        # with col_a:
        #     y1_cols = st.multiselect("Select Y-Axis 1 (Left)", numeric_columns, default=["units", "offtake"], key="y_axis_left_")
        # with col_b:
        #     chart_type = st.selectbox("Chart Type", ["Area", "Line", "Bar", "Scatter", "Spline", "Step", "Dot", "Combo"])
        # with col_c:
        #     y2_cols = st.multiselect("Select Y-Axis 2 (Right)", numeric_columns, default=["asp"], key="y_axis_right_")

        with show_loader("Rendering chart..."):
            render_chart(df)

    @staticmethod
    def compare_charts(dataframe_1, dataframe_2):
        df_1 = dataframe_1
        df_2 = dataframe_2

        # Get common columns
        common_columns = list(set(df_1.columns).intersection(df_2.columns))

        # Multiselect to choose which columns to filter on
        selected_cols = st.multiselect(
            "Select common columns to filter",
            options=common_columns,
            default=[]
        )

        # Apply filters dynamically
        filters = {}
        for col in selected_cols:
            unique_values = sorted(pd.concat([df_1[col], df_2[col]]).dropna().unique())
            selected_values = st.multiselect(f"Filter by values in '{col}'", unique_values)
            if selected_values:
                filters[col] = selected_values

        # Apply filters to both DataFrames
        for col, values in filters.items():
            df_1 = df_1[df_1[col].isin(values)]
            df_2 = df_2[df_2[col].isin(values)]


        # col_1, col_2 = st.columns([1, 1])
        #
        # with col_1:
        #     with show_loader("Loading data..."):
        #         render_chart(df_1)
        #
        # with col_2:
        #     with show_loader("Loading data..."):
        #         render_chart(df_2)

    @staticmethod
    def compare_grids(dataframe_1, dataframe_2):
        df_1 = dataframe_1
        df_2 = dataframe_2

        # Get common columns
        common_columns = list(set(df_1.columns).intersection(df_2.columns))

        # Multiselect to choose which columns to filter on
        selected_cols = st.multiselect(
            "Select common columns to filter",
            options=common_columns,  # Uses the list directly
            default=[]
        )

        # Apply filters dynamically
        filters = {}
        for col in selected_cols:
            unique_values = sorted(pd.concat([df_1[col], df_2[col]]).dropna().unique())
            selected_values = st.multiselect(f"Filter by values in '{col}'", unique_values)
            if selected_values:
                filters[col] = selected_values

        # Apply filters to both DataFrames
        for col, values in filters.items():
            df_1 = df_1[df_1[col].isin(values)]
            df_2 = df_2[df_2[col].isin(values)]

        col_1, col_2 = st.columns([1, 1])

        with col_1:
            with show_loader("Loading data..."):
                render_aggrid(df_1)

        with col_2:
            with show_loader("Loading data..."):
                render_aggrid(df_2)

    @staticmethod
    def compare_grids_charts(dataframe_1, dataframe_2):
        df_1 = dataframe_1
        df_2 = dataframe_2

        # Get common columns
        common_columns = list(set(df_1.columns).intersection(df_2.columns))

        # Multiselect to choose which columns to filter on
        selected_cols = st.multiselect(
            "Select common columns to filter",
            options=common_columns,  # Uses the list directly
            default=[]
        )

        # Apply filters dynamically
        filters = {}
        for col in selected_cols:
            unique_values = sorted(pd.concat([df_1[col], df_2[col]]).dropna().unique())
            selected_values = st.multiselect(f"Filter by values in '{col}'", unique_values)
            if selected_values:
                filters[col] = selected_values

        # Apply filters to both DataFrames
        for col, values in filters.items():
            df_1 = df_1[df_1[col].isin(values)]
            df_2 = df_2[df_2[col].isin(values)]

        col_1, col_2 = st.columns([1, 1])

        with col_1:

            tab1, tab2 = st.tabs(["DATA", "CHART"])

            with tab1:
                with show_loader("Loading data..."):
                    render_aggrid(df_1)

            with tab2:
                pass
                # self.chart()

        with col_2:
            tab1, tab2 = st.tabs(["DATA", "CHART"])

            with tab1:
                with show_loader("Loading data..."):
                    render_aggrid(df_1)

            with tab2:
                pass
                # self.chart()
