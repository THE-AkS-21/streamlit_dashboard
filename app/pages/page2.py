import streamlit as st

def show_second_page():
    st.title("Page 2")
    st.write("This is the content of page 2")

    st.button("Log out", on_click=st.logout)