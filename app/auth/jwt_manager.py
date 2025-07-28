import jwt
from jwt import DecodeError, ExpiredSignatureError
import streamlit as st

SECRET_KEY = st.secrets["jwt"]["jwt_secret"]
ALGORITHM = "HS256"

def decode_jwt(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        st.warning("🔒 Token expired. Please log in again.")
        return None
    except DecodeError:
        st.error("❌ Invalid token.")
        return None
