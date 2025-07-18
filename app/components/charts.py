import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_lightweight_charts import renderLightweightCharts
from typing import List, Dict, Any


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
        cols = st.columns(len(metrics))
        for col, metric in zip(cols, metrics):
            with col:
                st.metric(
                    label=metric["label"],
                    value=metric["value"],
                    delta=metric.get("delta")
                )

    # ------------------- 🔹 LIGHTWEIGHT BASELINE CHART -------------------
    @staticmethod
    def render_lightweight_baseline_chart(df: pd.DataFrame, key="baseline_chart"):
        if df.empty or not {"time", "value"}.issubset(df.columns):
            st.warning("No valid data for baseline chart.")
            return

        df["time"] = pd.to_datetime(df["time"], errors="coerce")
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
        df = df.dropna(subset=["time", "value"]).sort_values("time")

        chart_data = [
            {"time": int(row["time"].timestamp()), "value": row["value"]}
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
            "layout": {"textColor": 'black', "background": {"type": 'solid', "color": 'white'}},
            "height": 400,
            "timeScale": {"timeVisible": True}
        }

        renderLightweightCharts([{"chart": chart, "series": series}], key=key)

    # ------------------- 🔹 TIME SERIES (LIGHTWEIGHT) -------------------
    @staticmethod
    def orders_chart(df: pd.DataFrame, key: str = "chart_1") -> None:
        if df.empty or not {"time", "value"}.issubset(df.columns):
            st.warning("No valid data for rendering chart.")
            return

        df["time"] = pd.to_datetime(df["time"], errors="coerce").dt.strftime('%Y-%m-%d')
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
        df = df.dropna(subset=["time", "value"]).sort_values("time")

        chart_data = df[["time", "value"]].to_dict("records")

        renderLightweightCharts(
            charts=[{
                "chart": {
                    "height": 400,
                    "layout": {"textColor": "black", "background": {"type": "solid", "color": "white"}},
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

    # ------------------- 🔹 UNITS OVER TIME -------------------
    def units_over_time(self) -> None:
        if not {"valuationdate", "units"}.issubset(self.df.columns):
            st.warning("Required columns not found.")
            return

        df = self.df.copy()
        df["valuationdate"] = pd.to_datetime(df["valuationdate"], errors="coerce")
        df = df.dropna(subset=["valuationdate", "units"])
        daily_units = df.groupby("valuationdate")["units"].sum().reset_index()

        fig = px.line(daily_units, x="valuationdate", y="units", title="Units Over Time", markers=True)
        st.plotly_chart(fig, use_container_width=True)

    # ------------------- 🔹 BAR CHARTS -------------------
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
        self._bar_chart("category", "Units by Category")

    def units_by_subcategory(self) -> None:
        self._bar_chart("subcategory", "Units by Subcategory")

    # ------------------- 🔹 PIE CHART -------------------
    def units_by_sku(self) -> None:
        if not {"whsku", "units"}.issubset(self.df.columns):
            st.warning("Required columns not found.")
            return

        df = self.df.dropna(subset=["whsku", "units"])
        unique_skus = df["whsku"].unique().tolist()
        selected_skus = st.multiselect("Select SKUs to display", unique_skus, default=unique_skus[:10])

        if not selected_skus:
            st.warning("Please select at least one SKU.")
            return

        agg_df = df[df["whsku"].isin(selected_skus)].groupby("whsku")["units"].sum().reset_index()
        agg_df = agg_df.sort_values("units", ascending=False).head(20)

        fig = px.pie(agg_df, names="whsku", values="units", title="Units by SKU", hole=0.3)
        fig.update_traces(textinfo="label+percent+value", hovertemplate="SKU: %{label}<br>Units: %{value}<extra></extra>")
        st.plotly_chart(fig, use_container_width=True)

    # ------------------- 🔹 Combined ASP (Bar), Units & Offtake (Area) Lightweight Chart -------------------

    def asp_units_offtake_chart(self, key="asp_units_offtake_chart") -> None:
        """
        Combines a Histogram and Area chart to visualize Units and Offtake (if available) over time per SKU.
        """
        if not {"valuationdate", "units", "whsku"}.issubset(self.df.columns):
            st.warning("Required columns (valuationdate, units, whsku) not found.")
            return

        df = self.df.copy()
        df["valuationdate"] = pd.to_datetime(df["valuationdate"], errors="coerce")
        df["units"] = pd.to_numeric(df["units"], errors="coerce")

        if "offtake" in df.columns:
            df["offtake"] = pd.to_numeric(df["offtake"], errors="coerce")

        df = df.dropna(subset=["valuationdate", "units", "whsku"])

        # Filter by SKU selection
        unique_skus = sorted(df["whsku"].dropna().unique())
        selected_skus = st.multiselect("Select SKUs to display", unique_skus, default=unique_skus[:5],
                                       key=f"{key}_skus")

        if not selected_skus:
            st.warning("Please select at least one SKU.")
            return

        df = df[df["whsku"].isin(selected_skus)]

        # Aggregate units/offtake per day
        agg_df = df.groupby(["valuationdate", "whsku"]).agg(
            {"units": "sum", "offtake": "sum" if "offtake" in df.columns else "first"}).reset_index()

        fig = px.histogram(
            agg_df,
            x="valuationdate",
            y="units",
            color="whsku",
            barmode="stack",
            nbins=30,
            title="Units Sold (Histogram) + Offtake (Area if present)"
        )

        fig.update_traces(opacity=0.7, marker_line_width=0)

        if "offtake" in agg_df.columns and not agg_df["offtake"].isna().all():
            for sku in selected_skus:
                sku_df = agg_df[agg_df["whsku"] == sku]
                fig.add_scatter(
                    x=sku_df["valuationdate"],
                    y=sku_df["offtake"],
                    mode="lines+markers",
                    name=f"{sku} Offtake",
                    yaxis="y2"
                )

            fig.update_layout(
                yaxis2=dict(
                    title="Offtake",
                    overlaying="y",
                    side="right",
                    showgrid=False
                )
            )

        fig.update_layout(xaxis_title="Date", yaxis_title="Units")
        st.plotly_chart(fig, use_container_width=True)

    # ------------------- 🔹 SUNBURST CHART -------------------
    def sunburst_chart(self) -> None:
        chart_data, error = self.prepare_chart_data("Sunburst")
        if error:
            st.warning(error)
            return

        fig = px.sunburst(
            chart_data,
            path=["Category", "Subcategory", "SKU"],
            values="Units",
            title="Sunburst Chart: Category > Subcategory > SKU"
        )
        fig.update_traces(textinfo="label+percent+value", hovertemplate="<b>%{label}</b><br>Units: %{value}<extra></extra>")
        st.plotly_chart(fig, use_container_width=True)

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
