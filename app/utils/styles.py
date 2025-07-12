def load_css():
    return """
    <style>
    h2 {
        color: #2962FF;
    }
    .stButton>button {
        border-radius: 6px;
        background-color: #2962FF;
        color: white;
        padding: 8px 20px;
        transition: background-color 0.25s ease;
    }
    .stButton>button:hover {
        background-color: #0039cb;
    }
    .chart-container {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
    }
    .metric-container {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
    }
    /* Clean general utilities if needed */
    .text-muted {
        color: #6B7280;
        font-size: 0.85rem;
    }
    </style>
    """
