import streamlit as st

def render_sidebar_toggle_script():
    st.markdown("""
    <script>
    window.addEventListener("load", function() {
        const sidebar = document.getElementById("custom-sidebar");
        const content = document.getElementById("custom-content");
        const hamburger = document.getElementById("hamburger-toggle");

        function adjustContentMargin() {
            if (window.innerWidth > 768) {
                if (sidebar.classList.contains("show") || sidebar.matches(":hover")) {
                    content.style.marginLeft = "200px";
                } else {
                    content.style.marginLeft = "70px";
                }
            }
        }

        // Hover adjustment (desktop only)
        if (window.innerWidth > 768 && sidebar && content) {
            sidebar.addEventListener("mouseenter", adjustContentMargin);
            sidebar.addEventListener("mouseleave", adjustContentMargin);
        }

        // Hamburger click
        if (hamburger && sidebar && content) {
            hamburger.addEventListener("click", function(event) {
                event.stopPropagation();
                sidebar.classList.toggle("show");
                adjustContentMargin();
            });
        }

        // Window resize — keep margins in sync
        window.addEventListener("resize", adjustContentMargin);

        // Initial state sync
        adjustContentMargin();
    });
    </script>
    """, unsafe_allow_html=True)
