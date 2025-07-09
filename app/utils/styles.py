# app/utils/styles.py
def load_css():
    return """
    <style>
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

    .sidebar-hover:hover + .main-content {
        filter: blur(5px);
    }

    .main-content {
        transition: filter 0.3s ease;
    }

    .nav-item {
        padding: 1rem;
        cursor: pointer;
        transition: background-color 0.3s;
    }

    .nav-item:hover {
        background-color: #f0f2f6;
    }

    .stButton>button {
        width: 100%;
    }

    .chart-container {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    .user-info {
        padding: 1rem;
        border-bottom: 1px solid #eee;
    }
    </style>
    """
