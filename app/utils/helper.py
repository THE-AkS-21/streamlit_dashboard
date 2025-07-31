# Any additional utility functions can go here

def greet_user(name: str) -> str:
    """Returns a greeting message."""
    return f"Hello, {name}! Welcome to the Streamlit API Demo."

def _meta_key(start, end):
    return f"dashboard_metadata_{start}_{end}"

