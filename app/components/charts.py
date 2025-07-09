import streamlit as st
from typing import List, Dict, Any
from streamlit_lightweight_charts import renderLightweightCharts
import pandas as pd

class ChartComponent:
    @staticmethod
    def metric_cards(metrics: List[Dict[str, Any]]):
        cols = st.columns(len(metrics))
        for col, metric in zip(cols, metrics):
            with col:
                st.metric(
                    label=metric['label'],
                    value=metric['value'],
                    delta=metric.get('delta')
                )

    @staticmethod
    def orders_chart(df: pd.DataFrame, key="chart_1"):
        if df.empty:
            st.warning("No data to display.")
            return

        df = df.copy()
        df['time'] = pd.to_datetime(df['time']).dt.strftime('%Y-%m-%d')
        df = df.sort_values('time')
        df = df.dropna(subset=['value'])
        df['value'] = df['value'].astype(float)

        chart_data = df[['time', 'value']].to_dict('records')

        if not chart_data:
            st.warning("No valid chart data available.")
            return

        chart_config = {
            "height": 400,
            "layout": {
                "textColor": 'black',
                "background": {
                    "type": 'solid',
                    "color": 'white'
                }
            },
            "timeScale": {
                "timeVisible": True
            }
        }

        renderLightweightCharts(
            charts=[{
                "chart": chart_config,
                "series": [{
                    "type": 'Area',
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
