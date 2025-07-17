import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_lightweight_charts import renderLightweightCharts
from typing import List, Dict, Any


class ChartComponent:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    # ------------------- 🔹 METRIC CARDS -------------------
    @staticmethod
    def metric_cards(metrics: List[Dict[str, Any]]) -> None:
        cols = st.columns(len(metrics))
        for col, metric in zip(cols, metrics):
            with col:
                st.metric(
                    label=metric["label"],
                    value=metric["value"],
                    delta=metric.get("delta")
                )

    # ------------------- 🔹 CUSTOM BASELINE CHART -------------------
    @staticmethod
    def render_lightweight_baseline_chart(df: pd.DataFrame, key="baseline_chart"):
        if df.empty or not {"time", "value"}.issubset(df.columns):
            st.warning("No valid data for baseline chart.")
            return

        df = df.copy()
        df["time"] = pd.to_datetime(df["time"], errors="coerce")
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
        df = df.dropna(subset=["time", "value"]).sort_values("time")

        if df.empty:
            st.warning("No valid chart data.")
            return

        chart_data = [
            {
                "time": int(pd.Timestamp(row["time"]).timestamp()),
                "value": row["value"]
            }
            for _, row in df.iterrows()
        ]

        series = [{
            "type": "Baseline",
            "data": chart_data,
            "options": {
                "baseValue": {"type": "price", "price": df["value"].mean()},
                "topLineColor": 'rgba(38, 166, 154, 1)',
                "topFillColor1": 'rgba(38, 166, 154, 0.28)',
                "topFillColor2": 'rgba(38, 166, 154, 0.05)',
                "bottomLineColor": 'rgba(239, 83, 80, 1)',
                "bottomFillColor1": 'rgba(239, 83, 80, 0.05)',
                "bottomFillColor2": 'rgba(239, 83, 80, 0.28)'
            }
        }]

        chart = {
            "layout": {
                "textColor": 'black',
                "background": {
                    "type": 'solid',
                    "color": 'white'
                }
            },
            "height": 400,
            "timeScale": {"timeVisible": True}
        }

        renderLightweightCharts([{"chart": chart, "series": series}], key=key)

    # ------------------- 🔹 TIME SERIES CHART -------------------
    @staticmethod
    def orders_chart(df: pd.DataFrame, key: str = "chart_1") -> None:
        if df.empty or not {"time", "value"}.issubset(df.columns):
            st.warning("No valid data for rendering chart.")
            return

        df['time'] = pd.to_datetime(df['time'], errors='coerce').dt.strftime('%Y-%m-%d')
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        df = df.dropna(subset=['time', 'value']).sort_values('time')

        chart_data = df[['time', 'value']].to_dict('records')
        if not chart_data:
            st.warning("No valid chart data available.")
            return

        renderLightweightCharts(
            charts=[{
                "chart": {
                    "height": 400,
                    "layout": {
                        "textColor": "black",
                        "background": {"type": "solid", "color": "white"}
                    },
                    "timeScale": {"timeVisible": True}
                },
                "series": [{
                    "type": "Area",
                    "data": chart_data,
                    "options": {
                        "topColor": "rgba(41, 98, 255, 0.3)",
                        "bottomColor": "rgba(41, 98, 255, 0.0)",
                        "lineColor": "#2962FF",
                        "lineWidth": 2
                    }
                }]
            }],
            key=key
        )

    # ------------------- 🔹 LINE CHART: UNITS OVER TIME -------------------
    def units_over_time(self) -> None:
        if not {"valuationdate", "units"}.issubset(self.df.columns):
            st.warning("Required columns not found.")
            return

        df = self.df.copy()
        df['valuationdate'] = pd.to_datetime(df['valuationdate'], errors='coerce')
        df = df.dropna(subset=['valuationdate', 'units'])
        daily_units = df.groupby('valuationdate')['units'].sum().reset_index()

        fig = px.line(daily_units, x='valuationdate', y='units', title='Units Over Time', markers=True)
        st.plotly_chart(fig, use_container_width=True)

    # ------------------- 🔹 BAR CHART: CATEGORY / SUBCATEGORY -------------------
    def _bar_chart(self, group_col: str, title: str) -> None:
        if group_col not in self.df.columns:
            st.warning(f"'{group_col}' column not found.")
            return

        df = self.df.dropna(subset=[group_col, 'units'])
        agg_df = df.groupby(group_col)['units'].sum().reset_index()

        fig = px.bar(agg_df, x=group_col, y='units', title=title, text='units')
        fig.update_traces(textposition='auto')
        st.plotly_chart(fig, use_container_width=True)

    def units_by_category(self) -> None:
        self._bar_chart(group_col='category', title='Units by Category')

    def units_by_subcategory(self) -> None:
        self._bar_chart(group_col='subcategory', title='Units by Subcategory')

    # ------------------- 🔹 PIE CHART: UNITS BY SKU -------------------
    def units_by_sku(self) -> None:
        if 'whsku' not in self.df.columns or 'units' not in self.df.columns:
            st.warning("Required columns not found.")
            return

        df = self.df.dropna(subset=['whsku', 'units'])
        unique_skus = df['whsku'].unique().tolist()
        selected_skus = st.multiselect("Select SKUs to display", unique_skus, default=unique_skus[:10])

        if not selected_skus:
            st.warning("Please select at least one SKU.")
            return

        agg_df = df[df['whsku'].isin(selected_skus)].groupby('whsku')['units'].sum().reset_index()
        agg_df = agg_df.sort_values(by='units', ascending=False).head(20)

        fig = px.pie(
            agg_df,
            names='whsku',
            values='units',
            title='Units Distribution by SKU',
            hole=0.3
        )
        fig.update_traces(
            textinfo='label+percent+value',
            hovertemplate='SKU: %{label}<br>Units: %{value}<extra></extra>'
        )
        st.plotly_chart(fig, use_container_width=True)

    # ------------------- 🔹 SUNBURST CHART: CATEGORY > SUBCATEGORY -------------------
    def sunburst_chart(self) -> None:
        required_cols = {'category', 'subcategory', 'units'}
        if not required_cols.issubset(self.df.columns):
            st.warning("Required columns for sunburst not found.")
            return

        df = self.df.dropna(subset=required_cols)
        agg_df = df.groupby(['category', 'subcategory'])['units'].sum().reset_index()

        fig = px.sunburst(
            agg_df,
            path=['category', 'subcategory'],
            values='units',
            title='Category/Subcategory Sunburst'
        )
        fig.update_traces(
            hovertemplate='<b>%{label}</b><br>Units: %{value}<extra></extra>',
            textinfo='label+percent+value'
        )
        st.plotly_chart(fig, use_container_width=True)



        # ------------------- 🔹 DYNAMIC CHART -------------------

    def render_dynamic_chart(self, x_axis: str, y_axis: str, chart_type: str = "Line") -> None:
        if not x_axis or not y_axis:
            st.warning("Please select both X-axis and Y-axis.")
            return

        if x_axis not in self.df.columns or y_axis not in self.df.columns:
            st.error(f"Selected axes not found: {x_axis}, {y_axis}")
            return

        df = self.df.dropna(subset=[x_axis, y_axis])
        if df.empty:
            st.warning("No data available for selected axes.")
            return

        df[x_axis] = pd.to_datetime(df[x_axis],
                                    errors="coerce") if "date" in x_axis.lower() or pd.api.types.is_datetime64_any_dtype(
            df[x_axis]) else df[x_axis]
        df[y_axis] = pd.to_numeric(df[y_axis], errors="coerce")
        df = df.dropna(subset=[x_axis, y_axis])

        df.rename(columns={x_axis: "time", y_axis: "value"}, inplace=True)

        if chart_type == "Line":
            self.render_lightweight_baseline_chart(df)
            return

        # Special handling for other chart types
        if chart_type == "Pie":
            pie_df = df.groupby("time")["value"].sum().reset_index()
            fig = px.pie(pie_df, names="time", values="value", title="Pie Chart")
            fig.update_traces(textinfo="label+percent+value")
            st.plotly_chart(fig, use_container_width=True)
            return

        if chart_type == "Box":
            fig = px.box(df, x="time", y="value", title="Box Plot Over Time")
            st.plotly_chart(fig, use_container_width=True)
            return

        if chart_type == "Histogram":
            fig = px.histogram(df, x="value", nbins=30, title="Histogram of Values")
            st.plotly_chart(fig, use_container_width=True)
            return

        if chart_type == "Sunburst":
            if not {'category', 'subcategory', 'units'}.issubset(self.df.columns):
                st.warning("Required columns for sunburst not found.")
                return
            agg_df = self.df.groupby(['category', 'subcategory'])['units'].sum().reset_index()
            fig = px.sunburst(
                agg_df,
                path=['category', 'subcategory'],
                values='units',
                title='Category/Subcategory Sunburst'
            )
            fig.update_traces(textinfo='label+percent+value')
            st.plotly_chart(fig, use_container_width=True)
            return

        # Default chart types (Bar, Area, Scatter)
        chart_map = {
            "Bar": px.bar,
            "Area": px.area,
            "Scatter": px.scatter,
        }

        chart_func = chart_map.get(chart_type)
        if not chart_func:
            st.error(f"Unsupported chart type: {chart_type}")
            return

        fig = chart_func(
            df,
            x="time",
            y="value",
            title=f"{chart_type} Chart: value vs time",
            text="value" if chart_type in ["Bar", "Scatter"] else None
        )

        if chart_type in ["Bar", "Scatter"]:
            if chart_type == "bar":
                fig.update_traces(textposition="auto")
            elif chart_type == "scatter":
                fig.update_traces(textposition="top center")

        st.plotly_chart(fig, use_container_width=True)


