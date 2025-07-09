import streamlit as st

from app.utils.basic_api import add_numbers
from app.utils.helper import greet_user


def show_first_page():
    # Title of the app
    st.title("ADD TWO NUMBERS")

    st.divider()

    # Text input for user name
    st.success(greet_user(st.user.name))

    # Number inputs for API function
    num1 = st.number_input("Enter first number:", value=2.0)
    num2 = st.number_input("Enter second number:", value=1.0)

    # Button to call API function
    if st.button("Add Numbers"):
        result = add_numbers(num1, num2)
        st.toast("Your numbers were added.")
        st.write(f"The sum of {num1} and {num2} is **{result}**")

    st.button("Log out", on_click=st.logout)