import streamlit as st

def apply_global_styles():
    st.markdown("""
    <style>
    :root {
        --main-bg: #F9FAFB;
        --accent: #00AEEF;
        --sidebar-bg: #F3F4F6;
        --hover-bg: #E0E7FF;
        --text-main: #111827;
        --text-secondary: #374151;
    }

    html, body, main, section.main, section.main > div.block-container,
    [data-testid="stAppViewContainer"],
    [data-testid="stVerticalBlock"],
    [data-testid="stHorizontalBlock"],
    [data-testid="stMarkdownContainer"] {
        margin: 0 !important;
        padding: 0 !important;
    }
    h1, h2, h3, h4, h5, h6 {
        margin: 0 !important;
    }
    [data-testid="stMarkdownHeadingContainer"] a {
        display: none !important;
    }

    /* ===== Navbar ===== */
    .custom-navbar {
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
    }
    .navbar-left {
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .navbar-logo {
        width: 22px;
        height: 22px;
        border-radius: 20%;
        object-fit: cover;
    }
    .navbar-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: var(--accent);
        margin: 0;
    }
    .hamburger {
        width: 24px;
        height: 24px;
        cursor: pointer;
        display: none;
    }
    @media screen and (max-width: 768px) {
      .hamburger {
        display: block;
        position: fixed;
        top: 10px;
        left: 10px;
        z-index: 1200;
      }
    
      .custom-navbar {
        background: transparent;
        height: 0;
        width: 0;
        overflow: hidden;
        position: static;
      }
    
      .toolbar {
        display: none;
      }
    
      .custom-sidebar {
        top: 0;
        left: -180px;
        width: 180px;
      }
    
      .custom-sidebar.show {
        left: 0;
      }
    
      .custom-content {
        margin-left: 0;
      }
    
      .custom-sidebar .sidebar-label {
        opacity: 1;
      }
    
      #mobile-toolbar-items {
        display: block;
        margin-top: 10px;
      }
    }

    /* ===== Toolbar ===== */
    .toolbar {
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
    }
    .toolbar-btn, .toolbar-dropdown {
        background: transparent;
        border: none;
        color: var(--text-secondary);
        font-size: 0.72rem;
        cursor: pointer;
        padding: 2px 10px;
        transition: all 0.25s ease;
    }
    .toolbar-btn:hover, .toolbar-dropdown:hover {
        background: var(--hover-bg);
        color: var(--text-main);
        border-radius: 4px;
        transform: scale(1.05);
        box-shadow: 0 0 5px rgba(0, 174, 239, 0.15);
    }

    /* ===== Sidebar ===== */
    .custom-sidebar {
        position: fixed;
        top: 60px;
        left: 0;
        height: calc(100% - 60px);
        width: 50px;
        background: var(--sidebar-bg);
        transition: width 0.3s ease;
        overflow-x: hidden;
        z-index: 900;
        padding-top: 3px;
        display: flex;
        flex-direction: column;
        align-items: stretch;
    }
    .custom-sidebar a {
        text-decoration: none !important;
        color: inherit;
    }
    .custom-sidebar:hover {
        width: 180px;
    }
    .sidebar-item {
        display: flex;
        align-items: center;
        padding: 2px 2px;
        margin: 5px 2px;
        border-radius: 10px;
        color: var(--text-main);
        font-weight: 500;
        transition: background-color 0.25s, transform 0.2s;
        gap: 5px;
    }
    .sidebar-item:hover {
        background: var(--hover-bg);
        transform: translateX(3px);
        border-left: 4px solid var(--accent);
    }
    .sidebar-icon {
        width: 28px;
        height: 28px;
        min-width: 28px;
        min-height: 28px;
        object-fit: contain;
        flex-shrink: 0;
    }
    .sidebar-label {
        white-space: nowrap;
        font-size: 0.95rem;
        font-weight: 500;
        color: #60A5FA;
        opacity: 0;
        transition: opacity 0.3s ease, color 0.3s ease;
    }
    .custom-sidebar:hover .sidebar-label {
        opacity: 1;
    }
    .sidebar-item:hover .sidebar-label {
        color: var(--accent);
    }
    .sidebar-item.current-page {
        background: var(--hover-bg);
        border-left: 4px solid var(--accent);
        font-weight: 600;
    }
    .sidebar-item.current-page .sidebar-label {
        color: var(--accent);
    }
    @media screen and (max-width: 768px) {
      .hamburger {
        display: block;
        position: fixed;
        top: 10px;
        left: 10px;
        z-index: 1200;
      }
    
      .custom-navbar {
        background: transparent;
        height: 0;
        width: 0;
        overflow: hidden;
        position: static;
      }
    
      .toolbar {
        display: none;
      }
    
      .custom-sidebar {
        top: 0;
        left: -180px;
        width: 180px;
        transition: left 0.3s ease;
      }
    
      .custom-sidebar.show {
        left: 0;
      }
    
      .custom-content {
        margin-left: 0;
      }
    
      .custom-sidebar .sidebar-label {
        opacity: 1;
      }
    
      #mobile-toolbar-items {
        display: block;
        margin-top: 10px;
      }
    }

    /* ===== Content ===== */
    .custom-content {
        margin-top: 60px;
        margin-left: 70px;
        padding: 20px;
        transition: margin-left 0.3s ease;
    }
    .custom-sidebar:hover ~ .custom-content {
        margin-left: 180px;
    }

    /* ===== Mobile Responsive ===== */
    @media screen and (max-width: 768px) {
        .hamburger { display: block; }
        .navbar-left, .toolbar { display: none; }
        .custom-navbar { justify-content: flex-start; }
        .custom-sidebar {
            top: 30px;
            width: 180px;
        }
        .custom-sidebar.show {
            left: 0;
        }
        .custom-content { margin-left: 0; }
        .custom-sidebar .sidebar-label { opacity: 1; }
        #mobile-toolbar-items { display: block; margin-top: 10px; }
    }

    </style>
    """, unsafe_allow_html=True)
