import streamlit as st

def render_navbar_and_sidebar():
    st.markdown("""
        <style>
        /* Remove padding around the Streamlit app */
        .block-container {
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100%;
        }

        /* Fixed top navbar */
        .custom-navbar {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 60px;
            background-color: white;
            border-bottom: 2px solid #2962FF;
            display: flex;
            align-items: center;
            padding: 0 20px;
            z-index: 1000;
        }

        .custom-navbar h1 {
            margin: 0;
            font-size: 1.5rem;
            color: black;
        }

        /* Sidebar */
        .custom-sidebar {
            position: fixed;
            top: 60px;
            left: 0;
            width: 70px;
            height: calc(100% - 60px);
            background-color: white;
            border-right: 2px solid #2962FF;
            transition: width 0.3s;
            overflow-x: hidden;
            z-index: 900;
        }

        .custom-sidebar:hover {
            width: 220px;
        }

        .sidebar-item {
            padding: 16px;
            display: flex;
            align-items: center;
            cursor: pointer;
            color: black;
        }

        .sidebar-item:hover {
            background-color: #f0f2f6;
        }

        .sidebar-icon {
            font-size: 20px;
            margin-right: 12px;
            min-width: 30px;
            text-align: center;
        }

        .sidebar-label {
            opacity: 0;
            white-space: nowrap;
            transition: opacity 0.3s;
        }

        .custom-sidebar:hover .sidebar-label {
            opacity: 1;
        }

        /* Main Content */
        .custom-content {
            margin-top: 60px;
            margin-left: 70px;
            padding: 20px;
            transition: margin-left 0.3s ease;
        }

        .custom-sidebar:hover ~ .custom-content {
            margin-left: 220px;
        }

        </style>

        <div class="custom-navbar">
            <h1>🚀 BSC Dashboard</h1>
        </div>

        <div class="custom-sidebar">
            <div class="sidebar-item">
                <div class="sidebar-icon">🏠</div>
                <div class="sidebar-label">Home</div>
            </div>
            <div class="sidebar-item">
                <div class="sidebar-icon">📊</div>
                <div class="sidebar-label">Analytics</div>
            </div>
            <div class="sidebar-item">
                <div class="sidebar-icon">⚙️</div>
                <div class="sidebar-label">Settings</div>
            </div>
        </div>
        """, unsafe_allow_html=True)