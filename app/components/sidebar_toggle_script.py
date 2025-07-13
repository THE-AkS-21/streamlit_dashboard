import streamlit as st

def render_sidebar_toggle_script():
    st.markdown("""
    <script>
    window.addEventListener("load", function() {
        setTimeout(function() {
            const hamburger = document.getElementById("hamburger-toggle");
            const sidebar = document.getElementById("custom-sidebar");

            if (hamburger && sidebar) {
                console.log("Hamburger click listener attached");
                hamburger.addEventListener("click", function(event) {
                    event.stopPropagation();
                    sidebar.classList.toggle("show");
                });

                document.addEventListener("click", function(event) {
                    if (window.innerWidth <= 768) {
                        if (!sidebar.contains(event.target) && event.target !== hamburger) {
                            sidebar.classList.remove("show");
                        }
                    }
                });
            } else {
                console.log("Missing sidebar or hamburger", hamburger, sidebar);
            }
        }, 0);
    });
    </script>
    """, unsafe_allow_html=True)
