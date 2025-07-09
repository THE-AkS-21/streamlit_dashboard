# app/utils/cache_utils.py
import streamlit as st
from functools import wraps
from datetime import datetime, timedelta


def cache_data(ttl=3600):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}_{str(args)}_{str(kwargs)}"

            # Check if data exists in cache and is not expired
            if cache_key in st.session_state:
                cached_data, cached_time = st.session_state[cache_key]
                if datetime.now() - cached_time < timedelta(seconds=ttl):
                    return cached_data

            # If not in cache or expired, execute function
            result = func(*args, **kwargs)

            # Store in cache
            st.session_state[cache_key] = (result, datetime.now())

            return result

        return wrapper

    return decorator