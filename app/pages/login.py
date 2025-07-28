import base64
import streamlit as st
from app.api.user_api import authenticate_user
from app.auth.cookies import set_jwt_cookie, get_jwt_from_cookie
from app.components.loading_screen import loading_screen


def authenticate_from_cookie() -> bool:
    token = get_jwt_from_cookie()
    if not token:
        return False
    return True

# Load local image and encode as base64
def get_base64_bg(path):
    with open(path, "rb") as img_file:
        b64_string = base64.b64encode(img_file.read()).decode()
    return f"data:image/png;base64,{b64_string}"

# Get encoded image
bg_image = get_base64_bg("app/assets/images/bg_cover.jpg")

def show_login_page():
    st.set_page_config(page_title="Login", layout="wide")

    # ─── Custom CSS for Layout and Styling ────────────────
    st.markdown(f"""
        <style>
            html, body, [data-testid="stAppViewContainer"] {{
                height: 100vh !important;
                margin: 0;
                padding: 0;
                background: url("{bg_image}") no-repeat center center fixed;
                background-size: cover;
                display: flex;
                justify-content: center;
                align-items: center;
            }}
            .background-blur::before {{
                content: "";
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: inherit;
                backdrop-filter: blur(5px);
                z-index: 0;
            }}

            .login-card {{
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                z-index: 1;
                background: white;
                padding: 3rem 2rem;
                border-radius: 18px;
                box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
                width: 100%;
                max-width: 400px;
                text-align: center;
                font-family: 'Segoe UI', sans-serif;
            }}

            .login-title {{
                font-size: 26px;
                font-weight: 600;
                margin-bottom: 2.5rem;
                color: #1f2937;
            }}

            .google-btn:hover {{
                background-color: #357ae8;
            }}

            .google-icon {{
                height: 20px;
                width: 20px;
                background-image: url('https://upload.wikimedia.org/wikipedia/commons/4/4a/Logo_2013_Google.png');
                background-size: cover;
                background-repeat: no-repeat;
            }}
        </style>
    """, unsafe_allow_html=True)

    # Wrap main layout in blurred background
    st.markdown('<div class="background-blur">', unsafe_allow_html=True)

    if "login_attempted" not in st.session_state:
        st.session_state.login_attempted = False

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if "show_loader" not in st.session_state:
        st.session_state.show_loader = False

    if not st.session_state.authenticated and not st.session_state.show_loader:
        with st.container():
            # ─── Login Card ───────────────────────────────
            st.markdown("<br><br><br><br>", unsafe_allow_html=True)

            col1, col2, col3 = st.columns([2.5, 2, 1])
            with col2:
            # Google Sign-In Button
                if st.button("  Sign in with Google", key="google-login-btn"):
                    st.session_state.login_attempted = True
                    st.login()

    # Handle token generation only after login and user confirmed
    if st.session_state.login_attempted and st.user and not st.session_state.authenticated:
        user_email = st.user.email
        token = authenticate_user(user_email) # api call
        if token:
            set_jwt_cookie(token) # cookie
            st.session_state.jwt_token = token
            st.session_state.show_loader = True
        else:
            st.error("❌ Token generation failed.")

        # ─── Loading Screen ───
    st.markdown('</div>', unsafe_allow_html=True)
