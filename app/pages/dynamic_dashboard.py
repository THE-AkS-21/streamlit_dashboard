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
    meta_key = f"dashboard_metadata_{start_date}_{end_date}"

    if meta_key not in st.session_state:
        st.session_state[meta_key] = _load_dashboard_metadata(start_date, end_date)

    return st.session_state[meta_key]

def render_content():
    render = Render()

    #---------------------START INJECTING COMPONENTS--------------------------#

    render.title('BOMBAY SHAVING COMPANY')
    render.filter()
    render.metric()
    render.grid()

def show_dynamic_dashboard():
    apply_global_styles()

    # Step 1: Get or set default filter dates in session
    if "filter_start" not in st.session_state:
        st.session_state["filter_start"] = DEFAULT_START_DATE
    if "filter_end" not in st.session_state:
        st.session_state["filter_end"] = datetime.today().date()

    start_date = st.session_state["filter_start"]
    end_date = st.session_state["filter_end"]

    # Step 2: Load dashboard metadata based on current filter dates
    metadata_df = get_dashboard_metadata(start_date, end_date)
    st.session_state["metadata_df"] = metadata_df

    # Step 3: Store start and end range from metadata if needed
    if "start_date" not in st.session_state:
        st.session_state["start_date"] = DEFAULT_START_DATE
    if "end_date" not in st.session_state:
        st.session_state["end_date"] = DEFAULT_END_DATE

    render_content()
