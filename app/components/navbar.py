import streamlit as st
from app.utils.icon_loader import load_icon

# @st.cache_resource(show_spinner=False)
def render_navbar():
    if "sidebar_open" not in st.session_state:
        st.session_state.sidebar_open = False

    st.markdown(f"""
        <div class="custom-navbar" >
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
    """, unsafe_allow_html=True)
