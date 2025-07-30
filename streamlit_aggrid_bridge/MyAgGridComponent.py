import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import json
import os

def render_component(data_df: pd.DataFrame, dist_dir: str):
    manifest_path = os.path.join(dist_dir, "manifest.json")
    if not os.path.exists(manifest_path):
        st.error(f"Manifest file not found in {dist_dir}")
        return

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    js_file = manifest.get("main.js")
    if not js_file:
        st.error(f"JS file not found in manifest for {dist_dir}")
        return

    js_path = os.path.join(dist_dir, js_file)
    if not os.path.exists(js_path):
        st.error(f"JS file not found: {js_path}")
        return

    with open(js_path, "r", encoding="utf-8") as f:
        js_content = f.read()

    data_json = data_df.to_json(orient="records")
    html_template = f"""
    <html>
      <head><script>window.gridData = {data_json};</script></head>
      <body>
        <div id="root"></div>
        <script type="module">{js_content}</script>
      </body>
    </html>
    """
    components.html(html_template, height=800, scrolling=True)

def render_aggrid(data_df: pd.DataFrame):
    render_component(data_df, "streamlit_aggrid_enterprise/frontend/dist/aggrid")

def render_chart(data_df: pd.DataFrame):
    render_component(data_df, "streamlit_aggrid_enterprise/frontend/dist/chart")
