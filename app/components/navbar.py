import streamlit as st
from app.utils.icon_loader import load_icon

@st.cache_resource(show_spinner=False)
def render_navbar():
    if "sidebar_open" not in st.session_state:
        st.session_state.sidebar_open = False

    st.markdown(f"""
        <style>
        :root {{
            --main-bg: #F9FAFB;
            --accent: #00AEEF;
            --sidebar-bg: #F3F4F6;
            --hover-bg: #E0E7FF;
            --text-main: #111827;
            --text-secondary: #374151;
        }}
        .custom-navbar {{
            position: fixed;
            top: 0;
            left: 0;
            height: 30px;
            width: 100%;
            background-color: var(--sidebar-bg);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 14px;
            z-index: 1000;
        }}
        .navbar-logo {{
            width: 22px;
            height: 22px;
        }}
        .navbar-title {{
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--accent);
            margin: 0;
        }}
        .hamburger {{
            width: 24px;
            height: 24px;
            cursor: pointer;
            display: none;
        }}
        .navbar-left {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        /* TOOLBAR STYLES */
        .toolbar {{
            position: fixed;
            top: 30px;
            left: 0;
            height: 30px;
            width: 100%;
            background-color: var(--sidebar-bg);
            display: flex;
            align-items: center;
            padding: 0 12px;
            gap: 8px;
            z-index: 999;
            
        }}
        .toolbar-dropdown {{
            appearance: none;
            height: 25px;
            background-color: var(--sidebar-bg);
            border-radius: 5px;
            padding: 2px 8px;
            font-size: 0.72rem;
            color: var(--text-secondary);
            transition: all 0.25s ease;
            cursor: pointer;
        }}
        .toolbar-dropdown:hover {{
            background-color: var(--hover-bg);
            color: var(--text-main);
        }}
        
        @media screen and (max-width: 768px) {{
            .hamburger {{
                display: block;
            }}
            .navbar-left {{
                display: none;
            }}
            .navbar-title {{
                flex: 1;
                text-align: center;
            }}
            .toolbar {{
                display: none;
            }}
        }}
        </style>

        <div class="custom-navbar">
            <img src="{load_icon('menu.png')}" class="hamburger" id="hamburger-toggle">
            <div class="navbar-left" style="display:flex; align-items:center; gap:10px;">
                <img src="{load_icon('logo.png')}" class="navbar-logo">
                <p class="navbar-title">Bombay Shaving Company</p>
            </div>
        </div>
        
        <!-- TOOLBAR -->
        <div class="toolbar">
            <select class="toolbar-dropdown" id="file-dropdown">
                <option>File</option>
                <option>New</option>
                <option>Open</option>
                <option>Save</option>
            </select>
            <select class="toolbar-dropdown" id="edit-dropdown">
                <option>Edit</option>
                <option>Undo</option>
                <option>Redo</option>
                <option>Cut</option>
            </select>
            <select class="toolbar-dropdown" id="view-dropdown">
                <option>View</option>
                <option>Zoom In</option>
                <option>Zoom Out</option>
            </select>
            <select class="toolbar-dropdown" id="insert-dropdown">
                <option>Insert</option>
                <option>Image</option>
                <option>Chart</option>
                <option>Table</option>
            </select>
            <select class="toolbar-dropdown" id="tools-dropdown">
                <option>Tools</option>
                <option>Settings</option>
                <option>Extensions</option>
            </select>
        </div>

        <script>
        window.addEventListener("load", function() {{
            setTimeout(function() {{
                const hamburger = document.getElementById("hamburger-toggle");
                const sidebar = document.getElementById("custom-sidebar");
        
                if (hamburger && sidebar) {{
                    hamburger.addEventListener("click", function() {{
                        sidebar.classList.toggle("show");
                    }});
                }}
            }}, 0);
        }});
        </script>

""", unsafe_allow_html=True)
