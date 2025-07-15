import streamlit as st

@st.cache_resource(show_spinner=False)
def render_toolbar(page):

    #"""Render toolbar dynamically based on current page"""
    # Define your toolbar menus per page
    page_toolbars = {
        "Dashboard": [
            ("New", "#"),
            ("Open", "#"),
            ("Save", "#")
        ],
        "Analytics": [
            ("Filter", "#"),
            ("Export", "#"),
            ("Compare", "#")
        ],
        "Settings": [
            ("Profile", "#"),
            ("Security", "#"),
            ("Logs", "#")
        ]
    }

    actions = page_toolbars.get(page, [])

    st.markdown(f"""
        <div class="toolbar">
            {"".join(f'<button class="toolbar-btn">{label}</button>' for label, _ in actions)}
        </div>
    """, unsafe_allow_html=True)

    return actions  # Return actions for sidebar merge
