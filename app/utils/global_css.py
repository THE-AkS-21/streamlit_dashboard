import streamlit as st
from app.config import config

def apply_global_styles():
    st.markdown(f"""
    <style>

    :root {{
        --main-bg: #F9FAFB;
        --accent: #00AEEF;
        --sidebar-bg: #F3F4F6;
        --hover-bg: #E0E7FF;
        --text-main: #111827;
        --text-secondary: #374151;
        --animation-speed: {config.animation_speed}s;
    }}

    /* ===== General Reset (Only for markdown blocks) ===== */
    header, footer {{
        visibility: hidden;
        height: 0;
    }}
    h1, h2, h3, h4, h5, h6 {{
        margin: 0 !important;
    }}
    [data-testid="stMarkdownContainer"],
    [data-testid="stMarkdownHeadingContainer"] {{
        margin: 0 !important;
        padding: 0 !important;
    }}
    section.main {{
        padding-top: 0 !important;
    }}
    [data-testid="stMarkdownHeadingContainer"] a {{
        display: none !important;
    }}

    /* ===== Navbar ===== */
    .custom-navbar {{
        position: fixed;
        top: 0;
        left: 0;
        height: 30px;
        width: 100%;
        background: var(--sidebar-bg);
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 14px;
        z-index: 1000;
    }}

    .navbar-left {{
        display: flex;
        align-items: center;
        gap: 8px;
    }}

    .navbar-logo {{
        width: 22px;
        height: 22px;
        border-radius: 20%;
        object-fit: cover;
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

    /* ===== Toolbar ===== */
    .toolbar {{
        position: fixed;
        top: 30px;
        left: 0;
        height: 30px;
        width: 100%;
        background: var(--sidebar-bg);
        display: flex;
        align-items: center;
        padding: 0 12px;
        gap: 8px;
        z-index: 999;
    }}

    .toolbar-btn, .toolbar-dropdown {{
        background: transparent;
        border: none;
        color: var(--text-secondary);
        font-size: 0.72rem;
        cursor: pointer;
        padding: 2px 10px;
        transition: all var(--animation-speed) ease;
    }}

    .toolbar-btn:hover, .toolbar-dropdown:hover {{
        background: var(--hover-bg);
        color: var(--text-main);
        border-radius: 4px;
        transform: scale(1.05);
        box-shadow: 0 0 5px rgba(0, 174, 239, 0.15);
    }}

    /* ===== Sidebar ===== */
    .custom-sidebar {{
        position: fixed;
        top: 60px;
        left: 0;
        height: calc(100% - 60px);
        width: 50px;
        background: var(--sidebar-bg);
        transition: width var(--animation-speed) ease;
        overflow-x: hidden;
        z-index: 900;
        padding-top: 3px;
        display: flex;
        flex-direction: column;
        align-items: stretch;
    }}

    .custom-sidebar a {{
        text-decoration: none !important;
        color: inherit;
    }}

    .custom-sidebar:hover {{
        width: 180px;
    }}

    .custom-sidebar.show {{
        width: 180px;
    }}

    .sidebar-item {{
        display: flex;
        align-items: center;
        padding: 3px 1px;
        margin: 3px 12px;
        border-radius: 10px;
        color: var(--text-main);
        font-weight: 500;
        gap: 5px;
        transition: background-color var(--animation-speed), transform var(--animation-speed);
    }}

    .sidebar-item:hover {{
        background: var(--hover-bg);
        transform: translateX(3px);
        border-left: 4px solid var(--accent);
    }}

    .sidebar-icon {{
        width: 28px;
        height: 28px;
        object-fit: contain;
        flex-shrink: 0;
        min-width: 28px;
        max-width: 28px;
        min-height: 28px;
        max-height: 28px;
        transition: all var(--animation-speed) ease;
        margin-right: 0;
    }}

    .sidebar-label {{
        display: inline-block;
        overflow: hidden;
        white-space: nowrap;
        font-size: 0.95rem;
        font-weight: 500;
        color: #60A5FA;
        margin-left: 12px;
        opacity: 0;
        transition: opacity var(--animation-speed), color var(--animation-speed);
    }}

    .custom-sidebar:hover .sidebar-label {{
        opacity: 1;
    }}

    .sidebar-item:hover .sidebar-label,
    .sidebar-item.current-page .sidebar-label {{
        color: var(--accent);
    }}

    .sidebar-item.current-page {{
        background: var(--hover-bg);
        border-left: 4px solid var(--accent);
        font-weight: 600;
    }}

    /* ===== Content Area ===== */
    .custom-content {{
        left: 50px;
        margin-left: 70px;
        padding: 30px;
        transition: margin-left var(--animation-speed) ease;
    }}

    @media screen and (min-width: 770px) {{
        #app-container .custom-sidebar:hover + .custom-content {{
            margin-left: 200px;
        }}
    }}

    /* ===== Metric Cards ===== */
    .metric-card {{
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
        text-align: center;
    }}

    .metric-label {{
        font-size: 0.8rem;
        color: var(--text-secondary);
    }}

    .metric-value {{
        font-size: 1.4rem;
        font-weight: 600;
        color: var(--text-main);
    }}

    /* ===== Buttons ===== */
    /* All Streamlit buttons */
    .stButton>button {{
        border-radius: 6px;
        background-color: #f1f5f9; /* light grey */
        color: #111827; /* dark text */
        padding: 8px 20px;
        border: 1px solid #e5e7eb;
        font-size: 0.875rem;
        transition: all 0.2s ease;
    }}
    
    /* On hover - BSC blue */
    .stButton>button:hover {{
        background-color: #2962FF;
        color: #ffffff;
        border-color: #2962FF;
        transform: scale(0.98);
    }}
    
    /* On click effect */
    .stButton>button:active {{
        transform: scale(0.96);
    }}
    
    /* Logout button wrapper */
    .sidebar-logout {{
        position: absolute;
        bottom: 20px;
        width: 100%;
        padding: 0 8px;
    }}
    
    /* Logout button specific style */
    .logout-btn {{
        width: 100%;
        background: #ffffff;
        color: #EF4444;
        border: 1px solid #EF4444;
        padding: 8px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        cursor: pointer;
        transition: all 0.2s ease;
    }}
    
    /* Logout button hover state */
    .logout-btn:hover {{
        background: #EF4444;
        color: #ffffff;
        border-color: #EF4444;
        transform: scale(0.98);
    }}
    
    /* On click effect */
    .logout-btn:active {{
        transform: scale(0.96);
    }}

    /* ===== Headings ===== */
    h2 {{
        color: #2962FF;
    }}

    /* ===== Text Utilities ===== */
    .text-muted {{
        color: #6B7280;
        font-size: 0.85rem;
    }}
    
    /* Container to center content */
    .settings-container {{
        max-width: 480px;
        margin: 60px auto;
        text-align: center;
    }}

    /* Page title */
    .page-title {{
        font-size: 1.75rem;
        margin-bottom: 24px;
        color: #111827;
    }}
    
    /* Profile card container */
    .profile-card {{
        background: #f9fafb;
        padding: 24px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 24px;
    }}
    
    /* Profile info items */
    .profile-item {{
        font-size: 0.95rem;
        padding: 8px 0;
        border-bottom: 1px solid #e5e7eb;
        color: #374151;
    }}
    
    .profile-item:last-child {{
        border-bottom: none;
    }}
    
    /* Center table content */
    div[data-testid="stDataFrameContainer"] table td,
    div[data-testid="stDataFrameContainer"] table th {{
        text-align: center !important;
        vertical-align: middle;
    }}
    
    /* Analytics container padding */
    .analytics-container {{
        margin-top: 30px;
    }}
    
    /* Sign out button — inherits your .stButton styling */
    div[data-testid="stButton"][key="signout_btn"] button {{
        width: 100%;
        background: #ffffff;
        color: #EF4444;
        border: 1px solid #EF4444;
        padding: 10px 14px;
        border-radius: 6px;
        font-size: 0.875rem;
        cursor: pointer;
        transition: all 0.2s ease;
    }}
    
    div[data-testid="stButton"][key="signout_btn"] button:hover {{
        background: #EF4444;
        color: #ffffff;
        border-color: #EF4444;
        transform: scale(0.98);
    }}
    
    div[data-testid="stButton"][key="signout_btn"] button:active {{
        transform: scale(0.96);
    }}


    /* ===== Mobile Styles ===== */
    @media screen and (max-width: 768px) {{
        .hamburger {{
            display: block;
            position: fixed;
            top: 10px;
            left: 10px;
            z-index: 1200;
        }}
        .navbar-left, .toolbar {{
            display: none;
        }}
        .custom-navbar {{
            background: transparent;
            height: 0;
            width: 0;
            overflow: hidden;
            position: static;
        }}
        .custom-sidebar {{
            top: 30px;
            left: -180px;
            width: 180px;
            transition: left var(--animation-speed) ease;
        }}
        .custom-sidebar.show {{
            left: 0;
        }}
        .custom-content {{
            margin: 50px 50px;
            padding: 30px;
            transition: left var(--animation-speed) ease;
        }}
        .custom-sidebar.show + .custom-content {{
            margin-left: 180px;
        }}
        .custom-sidebar .sidebar-label {{
            opacity: 1;
        }}
        #mobile-toolbar-items {{
            display: block;
            margin-top: 10px;
        }}
    }}

    </style>
    """, unsafe_allow_html=True)
