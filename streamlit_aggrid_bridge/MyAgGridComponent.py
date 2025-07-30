import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import os
import json

def render_aggrid(data_df: pd.DataFrame):
    """
    Renders an AG Grid React component inside Streamlit using built assets.
    Requires: `manifest.json`, built JS/CSS in `frontend/dist/`
    """

    # ─── Step 1: Paths ────────────────────────────────────────────────
    dist_dir = "streamlit_aggrid_enterprise/frontend/dist"
    manifest_path = os.path.join(dist_dir, "manifest.json")

    if not os.path.exists(manifest_path):
        st.error("❌ manifest.json not found. Run `npm run build` in the frontend directory.")
        return

    # ─── Step 2: Load Manifest ────────────────────────────────────────
    try:
        with open(manifest_path, "r") as f:
            manifest = json.load(f)
    except json.JSONDecodeError:
        st.error("❌ manifest.json is not a valid JSON file.")
        return

    js_file = manifest.get("main.js")
    # css_file = manifest.get("style.css")

    if not js_file or not os.path.exists(os.path.join(dist_dir, js_file)):
        st.error("❌ JavaScript file from manifest not found.")
        return

    # Optional: Embed CSS if available
    # css_tag = ""
    # css_path = os.path.join(dist_dir, css_file) if css_file else None
    # if css_file and os.path.exists(css_path):
    #     with open(css_path, "r") as f:
    #         css_content = f.read()
    #         css_tag = f"<style>{css_content}</style>"

    # ─── Step 3: Embed JS Inline ──────────────────────────────────────
    js_path = os.path.join(dist_dir, js_file)
    with open(js_path, "r", encoding="utf-8") as f:
        js_content = f.read()

    data_json = data_df.to_json(orient="records")

    html_template = f"""
    <html>
      <head>
        <script>
          window.gridData = {data_json};
        </script>
      </head>
      <body>
        <div id="root"></div>
        <script type="module">
            {js_content}
        </script>
      </body>
    </html>
    """

    # ─── Step 4: Render in Streamlit ──────────────────────────────────
    components.html(html_template, height=800, scrolling=True)
