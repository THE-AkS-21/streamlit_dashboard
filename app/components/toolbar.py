import streamlit as st

@st.cache_resource(show_spinner=False)
def render_toolbar(page):
    """Render toolbar dynamically based on current page"""

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

        <style>
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
        .toolbar-btn {{
            background: transparent;
            border: none;
            color: var(--text-secondary);
            font-size: 0.72rem;
            cursor: pointer;
            transition: all 0.25s ease;
            padding: 2px 10px;
        }}
        .toolbar-btn:hover {{
            background-color: var(--hover-bg);
            color: var(--text-main);
            border-radius: 4px;
            transform: scale(1.03);
        }}
        @media screen and (max-width: 768px) {{
            .toolbar {{
                display: none;
            }}
        }}
        </style>
    """, unsafe_allow_html=True)

    return actions  # Return actions for sidebar merge
