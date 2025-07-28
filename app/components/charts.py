import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict, Any
from app.utils.formatters import Formatters


def format_axis_ticks(series):
    tickvals = np.linspace(series.min(), series.max(), num=5)
    ticktext = [Formatters.format_indian_number(val) for val in tickvals]
    return tickvals, ticktext

class ChartComponent:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def prepare_chart_data(self, chart_type: str):
        if chart_type == "Sunburst":
            required_cols = ["category", "subcategory", "sku", "units"]
            missing = [col for col in required_cols if col not in self.df.columns]
            if missing:
                return None, f"Missing required columns for sunburst: {', '.join(missing)}"

            df = self.df.rename(columns={
                "category": "Category",
                "subcategory": "Subcategory",
                "sku": "SKU",
                "units": "Units"
            })

            return df[["Category", "Subcategory", "SKU", "Units"]], None
        return self.df.copy(), None

    # ------------------- 🔹 METRIC CARDS -------------------

    @staticmethod
    def metric_cards(metrics: List[Dict[str, Any]]) -> None:
        for metric in metrics:
            label = metric.get("label", "N/A")
            value = metric.get("value", "N/A")

            st.markdown(
                f"""
                <div class="metric-card">
                    <span class="metric-label">{label}:</span>
                    <span class="metric-value">{value}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

    # ------------------- 🔹 Multi Metrix Chart -------------------

    def multi_yaxis_line_chart(self, x_axis: str, y1_cols: list, y2_cols: list, key="multi_line_chart"):
        df = self.df.copy()
        df[x_axis] = pd.to_datetime(df[x_axis], errors="coerce")
        df.dropna(subset=[x_axis], inplace=True)

        # Group by date: sum for y1_cols, mean for y2_cols
        agg_dict = {col: "sum" for col in y1_cols}
        agg_dict.update({col: "mean" for col in y2_cols})
        df = df.groupby(x_axis, as_index=False).agg(agg_dict)

        fig = go.Figure()

        # Format axis ticks in Indian format
        def format_axis_ticks(series):
            tickvals = series.round(-2).dropna().unique()
            tickvals.sort()
            ticktext = [Formatters.format_indian_number(val) for val in tickvals]
            return tickvals, ticktext

        # Y1 axis ticks
        y1_vals, y1_text = format_axis_ticks(df[y1_cols[0]])
        # Y2 axis ticks
        y2_vals, y2_text = format_axis_ticks(df[y2_cols[0]])

        # Plot Y1 (left axis) with formatted hover
        for col in y1_cols:
            formatted = df[col].apply(Formatters.format_indian_number)
            fig.add_trace(go.Scatter(
                x=df[x_axis],
                y=df[col],
                mode="lines+markers",
                name=f"{col} (Y1)",
                yaxis="y1",
                text=formatted,
                hovertemplate=(
                    "<b>%{x|%d %b %Y}</b><br>"
                    f"{col} (Y1): %{{text}}<extra></extra>"
                )
            ))

        for col in y2_cols:
            formatted = df[col].apply(Formatters.format_indian_number)
            fig.add_trace(go.Scatter(
                x=df[x_axis],
                y=df[col],
                mode="lines+markers",
                name=f"{col} (Y2)",
                yaxis="y2",
                line=dict(dash="dot"),
                text=formatted,
                hovertemplate=(
                    "<b>%{x|%d %b %Y}</b><br>"
                    f"{col} (Y2): %{{text}}<extra></extra>"
                )
            ))

        # Layout
        fig.update_layout(
            title="Multi Y-Axis Line Chart",
            xaxis_title="Valuation Date",
            yaxis=dict(
                title="Y1 Axis",
                side="left",
                tickvals=y1_vals.tolist(),
                ticktext=y1_text
            ),
            yaxis2=dict(
                title="Y2 Axis",
                side="right",
                overlaying="y",
                tickvals=y2_vals.tolist(),
                ticktext=y2_text
            ),
            hovermode="x unified",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            margin=dict(t=40, b=40, l=40, r=40),
            height=500
        )

        st.plotly_chart(fig, use_container_width=True, key=key)

    # ------------------- 🔹 DYNAMIC CHART -------------------
    def render_dynamic_chart(self, x_axis: str, y_axis: str, chart_type: str = "Line") -> None:
        if not x_axis or not y_axis:
            st.warning("Please select both X and Y axes.")
            return

        if x_axis not in self.df.columns or y_axis not in self.df.columns:
            st.error(f"Invalid axes: {x_axis}, {y_axis}")
            return

        df = self.df.dropna(subset=[x_axis, y_axis])
        if df.empty:
            st.warning("No data available for selected axes.")
            return

        df[x_axis] = pd.to_datetime(df[x_axis], errors="coerce") if "date" in x_axis.lower() else df[x_axis]
        df[y_axis] = pd.to_numeric(df[y_axis], errors="coerce")
        df = df.dropna(subset=[x_axis, y_axis])
        df.rename(columns={x_axis: "time", y_axis: "value"}, inplace=True)

        # Special charts
        if chart_type == "Line":
            self.render_lightweight_baseline_chart(df)
            return

        elif chart_type == "Pie":
            pie_df = df.groupby("time")["value"].sum().reset_index()
            fig = px.pie(pie_df, names="time", values="value", title="Pie Chart")
            fig.update_traces(textinfo="label+percent+value")
            st.plotly_chart(fig, use_container_width=True)
            return

        elif chart_type == "Box":
            fig = px.box(df, x="time", y="value", title="Box Plot")
            st.plotly_chart(fig, use_container_width=True)
            return

        elif chart_type == "Histogram":
            fig = px.histogram(df, x="value", nbins=30, title="Histogram")
            st.plotly_chart(fig, use_container_width=True)
            return

        elif chart_type == "Sunburst":
            chart_data, error = self.prepare_chart_data("Sunburst")
            if chart_data is None:
                st.warning(error)
                return

            fig = px.sunburst(chart_data, path=["Category", "Subcategory", "SKU"], values="Units")
            fig.update_traces(textinfo="label+percent+value")
            st.plotly_chart(fig, use_container_width=True)
            return

        # Default charts
        chart_func_map = {
            "Bar": px.bar,
            "Area": px.area,
            "Scatter": px.scatter,
        }

        chart_func = chart_func_map.get(chart_type)
        if not chart_func:
            st.error(f"Unsupported chart type: {chart_type}")
            return

        fig = chart_func(df, x="time", y="value", title=f"{chart_type} Chart", text="value")
        st.plotly_chart(fig, use_container_width=True)
