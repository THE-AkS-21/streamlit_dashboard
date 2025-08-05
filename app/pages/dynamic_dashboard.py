import streamlit as st
from datetime import datetime
from app.components.custom_components import Render
from app.database.queries.dashboard_queries import DashboardQueries
from app.database.connection import db
from app.utils.global_css import apply_global_styles

DEFAULT_START_DATE = datetime(2025, 3, 1).date()
DEFAULT_END_DATE = datetime(2025, 4, 1).date()

@st.cache_data(ttl=3600, show_spinner=False)
def _load_dashboard_metadata(start_date: str, end_date: str):
    query = DashboardQueries.GET_DASHBOARD_FILTER_METADATA
    params = {"start_date": start_date, "end_date": end_date}
    return db.execute_query(query, params)

def get_dashboard_metadata(start_date: str, end_date: str):
    key = f"dashboard_metadata_{start_date}_{end_date}"
    if key not in st.session_state:
        st.session_state[key] = _load_dashboard_metadata(start_date, end_date)
    return st.session_state[key]

def render_content():
    st.session_state.setdefault("filter_start", DEFAULT_START_DATE)
    st.session_state.setdefault("filter_end", DEFAULT_END_DATE)

    # Now it is safe to access the keys
    start_date = st.session_state["filter_start"]
    end_date = st.session_state["filter_end"]

    # Now, instantiate Render by passing the dates
    render = Render(page_key="dynamic_dashboard", start_date=start_date, end_date=end_date)
    metadata = _load_dashboard_metadata(start_date, end_date)
    #------------------------ADD CONTENT-----------------------------#

    render.title("BOMBAY SHAVING COMPANY")

    render.filter()
    render.metric()
    # render.grid()
    # render.plot_chart()
    render.compare_grids(metadata,metadata)
    # render.compare_charts(metadata, metadata)
    # render.compare_grids_charts(metadata, metadata)
    # render.grid()

def show_dynamic_dashboard():
    apply_global_styles()

    st.session_state.setdefault("filter_start", DEFAULT_START_DATE)
    st.session_state.setdefault("filter_end", DEFAULT_END_DATE)

    start_date = st.session_state["filter_start"]
    end_date = st.session_state["filter_end"]

    st.session_state["metadata_df"] = get_dashboard_metadata(start_date, end_date)

    render_content()
