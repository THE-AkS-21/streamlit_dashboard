import streamlit as st
import time

def show_loader(message="Loading...", delay=0.5):
    placeholder = st.empty()

    with placeholder.container():
        st.markdown(f"""
            <div style="
                padding: 0.8rem;
                background-color: #f0f2f6;
                border: 1px solid #ccc;
                border-radius: 8px;
                font-weight: 500;
                display: flex;
                align-items: center;
                gap: 10px;
            ">
                <span class="loader" style="width: 16px; height: 16px; border: 2px solid #ccc; border-top: 2px solid #0366d6; border-radius: 50%; display: inline-block; animation: spin 0.6s linear infinite;"></span>
                <span>{message}</span>
            </div>

            <style>
                @keyframes spin {{
                    0% {{ transform: rotate(0deg); }}
                    100% {{ transform: rotate(360deg); }}
                }}
            </style>
        """, unsafe_allow_html=True)

    # Optional delay to simulate loading
    if delay:
        time.sleep(delay)

    return placeholder  # Return placeholder so caller can clear it later
