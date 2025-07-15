import streamlit as st

def render_content_start():
    st.markdown("""<div class="custom-content" style="margin: 0; padding: 0;">""", unsafe_allow_html=True)

def render_content_end():
    st.markdown("</div>", unsafe_allow_html=True)

def render_sidebar_content_sync_script():
    st.markdown("""
    <script>
    window.addEventListener("load", function() {
        const sidebar = document.getElementById("custom-sidebar");
        const content = document.querySelector(".custom-content");

        function adjustContentMargin() {
            if (window.innerWidth > 768) {
                if (sidebar.classList.contains("show") || sidebar.matches(":hover")) {
                    content.style.marginLeft = "180px";
                } else {
                    content.style.marginLeft = "70px";
                }
            }
        }

        if (sidebar && content) {
            // Adjust on sidebar hover
            sidebar.addEventListener("mouseenter", adjustContentMargin);
            sidebar.addEventListener("mouseleave", adjustContentMargin);

            // Adjust on sidebar class toggle (hamburger)
            const hamburger = document.getElementById("hamburger-toggle");
            if (hamburger) {
                hamburger.addEventListener("click", function(event) {
                    event.stopPropagation();
                    sidebar.classList.toggle("show");
                    adjustContentMargin();
                });
            }

            // Initial adjustment
            adjustContentMargin();
        }
    });
    </script>
    """, unsafe_allow_html=True)
