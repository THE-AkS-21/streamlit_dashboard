import streamlit as st

from pages import page1, page2, dashboard

def login_screen():
    st.header("WELCOME TO THE BSC")
    st.subheader("Please log in.")
    if st.button("Log in with Google"):
         st.login()

if not st.user.is_logged_in:
    login_screen()
else:
    pg = st.navigation([
        st.Page(dashboard.show_dashboard, title="DASHBOARD", icon="📊"),
        st.Page(page1.show_first_page, title="ADD 2 NUMBERS", icon="🏠"),
        st.Page(page2.show_second_page, title="SECOND PAGE", icon="📊"),
    ], position="top")

    # Run the selected page
    pg.run()



