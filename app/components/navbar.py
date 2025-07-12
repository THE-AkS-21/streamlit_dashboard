import streamlit as st

def render_navbar():
    st.markdown("""
        <style>
        .custom-navbar {
            position: fixed;
            top: 0;
            left: 0;
            height: 60px;
            width: 100%;
            background-color: #E5E7EB;
            border-bottom: 1px solid #D1D5DB;
            display: flex;
            align-items: center;
            padding: 0 20px;
            z-index: 1000;
        }
        .custom-navbar h1 {
            margin: 0;
            font-size: 1.5rem;
            color: black;
            flex: 1;
        }
        .hamburger {
            font-size: 26px;
            cursor: pointer;
            display: none;
        }
        @media screen and (max-width: 768px) {
            .hamburger {
                display: block;
            }
        }
        </style>

        <div class="custom-navbar">
            <h1>📊 BSC Dashboard</h1>
            <div class="hamburger" onclick="document.querySelector('.custom-sidebar').classList.toggle('show')">☰</div>
        </div>
    """, unsafe_allow_html=True)
