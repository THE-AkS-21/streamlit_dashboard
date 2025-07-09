def load_css():
    return """
    <style>
    .stButton>button {
        width: 100%;
    }

    .chart-container {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    .metric-container {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }

    /* Additional styles from your existing styles.py */
    .sidebar-hover {
        position: fixed;
        left: -300px;
        top: 0;
        height: 100vh;
        width: 300px;
        background-color: white;
        transition: all 0.3s ease;
        z-index: 1000;
        box-shadow: 2px 0 5px rgba(0,0,0,0.1);
    }

    .sidebar-hover:hover {
        left: 0;
    }

    .nav-item {
        padding: 1rem;
        cursor: pointer;
        transition: background-color 0.3s;
    }

    .nav-item:hover {
        background-color: #f0f2f6;
    }

    .user-info {
        padding: 1rem;
        border-bottom: 1px solid #eee;
    }
    </style>
    """