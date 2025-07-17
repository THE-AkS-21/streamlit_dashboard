import streamlit as st
import pandas as pd
from typing import List, Dict, Any, Optional
import plotly.express as px
from streamlit_lightweight_charts import renderLightweightCharts


class ChartComponent:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    # ─────────────────────────────────────────────────────────────
    # ✅ Metric Cards
    # ─────────────────────────────────────────────────────────────
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

    # ─────────────────────────────────────────────────────────────
    # ✅ Lightweight Orders Chart (Time vs Value)
    # ─────────────────────────────────────────────────────────────
    @staticmethod
    def orders_chart(df: pd.DataFrame, key: str = "chart_1") -> None:
        if df.empty:
            st.warning("No data to display.")
            return

        df = df.copy()
        df['time'] = pd.to_datetime(df['time'], errors='coerce').dt.strftime('%Y-%m-%d')
        df = df.dropna(subset=['time', 'value'])
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        df = df.dropna(subset=['value']).sort_values('time')

        chart_data = df[['time', 'value']].to_dict('records')
        if not chart_data:
            st.warning("No valid chart data available.")
            return

        chart_config = {
            "height": 400,
            "layout": {
                "textColor": "black",
                "background": {"type": "solid", "color": "white"},
            },
            "timeScale": {"timeVisible": True}
        }

        renderLightweightCharts(
            charts=[{
                "chart": chart_config,
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

    # ─────────────────────────────────────────────────────────────
    # ✅ Central Chart Dispatcher
    # ─────────────────────────────────────────────────────────────
    def render_chart(self, chart_type: str) -> None:
        chart_map = {
            "Units Over Time": self.units_over_time,
            "Units by Category": self.units_by_category,
            "Units by Subcategory": self.units_by_subcategory,
            "Units Distribution by SKU": self.units_by_sku,
            "Category/Subcategory Sunburst": self.sunburst_chart,
        }

        render_fn = chart_map.get(chart_type)
        if render_fn:
            render_fn()
        else:
            st.warning("Please select a valid chart type.")

    # ─────────────────────────────────────────────────────────────
    # 📈 Line Chart: Units over Time
    # ─────────────────────────────────────────────────────────────
    def units_over_time(self) -> None:
        df = self.df.copy()
        df['valuationdate'] = pd.to_datetime(df['valuationdate'], errors='coerce')
        df = df.dropna(subset=['valuationdate', 'units'])
        daily_units = df.groupby('valuationdate')['units'].sum().reset_index()

        fig = px.line(daily_units, x='valuationdate', y='units', title='Units Over Time')
        st.plotly_chart(fig, use_container_width=True)

    # ─────────────────────────────────────────────────────────────
    # 📊 Bar Chart: Units by Category
    # ─────────────────────────────────────────────────────────────
    def units_by_category(self) -> None:
        df = self.df.dropna(subset=['category', 'units'])
        agg_df = df.groupby('category')['units'].sum().reset_index()

        fig = px.bar(agg_df, x='category', y='units', title='Units by Category')
        st.plotly_chart(fig, use_container_width=True)

    # ─────────────────────────────────────────────────────────────
    # 📊 Bar Chart: Units by Subcategory
    # ─────────────────────────────────────────────────────────────
    def units_by_subcategory(self) -> None:
        df = self.df.dropna(subset=['subcategory', 'units'])
        agg_df = df.groupby('subcategory')['units'].sum().reset_index()

        fig = px.bar(agg_df, x='subcategory', y='units', title='Units by Subcategory')
        st.plotly_chart(fig, use_container_width=True)

    # ─────────────────────────────────────────────────────────────
    # 🥧 Pie Chart: Units Distribution by WHSKU
    # ─────────────────────────────────────────────────────────────
    def units_by_sku(self) -> None:
        df = self.df.dropna(subset=['whsku', 'units'])
        agg_df = df.groupby('whsku')['units'].sum().reset_index()
        top_skus = agg_df.sort_values(by='units', ascending=False).head(20)

        fig = px.pie(top_skus, names='whsku', values='units', title='Units Distribution by SKU')
        st.plotly_chart(fig, use_container_width=True)

    # ─────────────────────────────────────────────────────────────
    # 🌞 Sunburst Chart: Category → Subcategory
    # ─────────────────────────────────────────────────────────────
    def sunburst_chart(self) -> None:
        df = self.df.dropna(subset=['category', 'subcategory', 'units'])
        agg_df = df.groupby(['category', 'subcategory'])['units'].sum().reset_index()

        fig = px.sunburst(agg_df, path=['category', 'subcategory'], values='units', title='Category/Subcategory Sunburst')
        st.plotly_chart(fig, use_container_width=True)

    def render_dynamic_chart(self, x_axis, y_axis, chart_type="Line"):
        import plotly.express as px

        chart_map = {
            "Line": px.line,
            "Bar": px.bar,
            "Area": px.area,
            "Scatter": px.scatter,
        }

        chart_func = chart_map.get(chart_type)
        if not chart_func:
            st.warning(f"Unsupported chart type: {chart_type}")
            return

        fig = chart_func(self.df, x=x_axis, y=y_axis, title=f"{chart_type} Chart: {y_axis} vs {x_axis}")
        st.plotly_chart(fig, use_container_width=True)