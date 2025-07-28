import streamlit as st
import time

def show_loader(message="Loading...", duration=0.5):
    placeholder = st.empty()

    modern_loader_html = f"""
    <div style="
        padding: 1.2rem 1.5rem;
        background: linear-gradient(135deg, #ffffff, #f6f8fb);
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        font-family: 'Segoe UI', sans-serif;
        font-weight: 500;
        color: #333;
    ">
        <div style="margin-bottom: 10px; font-size: 1rem;"> {message}
        </div>
        <div style="
            width: 100%;
            height: 14px;
            background-color: #e0e0e0;
            border-radius: 8px;
            overflow: hidden;
            position: relative;
        ">
            <div style="
                height: 100%;
                width: 100%;
                background: linear-gradient(90deg, #4facfe, #00f2fe);
                animation: load-bar {duration}s linear forwards;
                transform: translateX(-100%);
            "></div>
        </div>
    </div>

    <style>
        @keyframes load-bar {{
            0% {{ transform: translateX(-100%); }}
            100% {{ transform: translateX(0%); }}
        }}
    </style>
    """

    placeholder.markdown(modern_loader_html, unsafe_allow_html=True)
    time.sleep(duration)
    return placeholder  # Clear with placeholder.empty()
