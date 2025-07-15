import streamlit as st

def render_content_start():
    """Begin the custom content area wrapper"""
    st.markdown(
        """<div class="custom-content" style="margin: 0; padding: 0;">""",
        unsafe_allow_html=True
    )


def render_content_end():
    """End the custom content area wrapper"""
    st.markdown("</div>", unsafe_allow_html=True)


def render_sidebar_content_sync_script():
    """Inject JS to dynamically sync sidebar state with content margin"""
    st.markdown("""
    <script>
    window.addEventListener("load", function() {
        const sidebar = document.getElementById("custom-sidebar");
        const content = document.querySelector(".custom-content");

        function adjustContentMargin() {
            if (!content || !sidebar) return;

            if (window.innerWidth > 768) {
                if (sidebar.classList.contains("show") || sidebar.matches(":hover")) {
                    content.style.marginLeft = "180px";
                } else {
                    content.style.marginLeft = "70px";
                }
            } else {
                // On mobile, margin is handled by media query CSS
                content.style.marginLeft = "0";
            }
        }

        if (sidebar && content) {
            sidebar.addEventListener("mouseenter", adjustContentMargin);
            sidebar.addEventListener("mouseleave", adjustContentMargin);

            const hamburger = document.getElementById("hamburger-toggle");
            if (hamburger) {
                hamburger.addEventListener("click", function(event) {
                    event.stopPropagation();
                    sidebar.classList.toggle("show");
                    adjustContentMargin();
                });
            }

            // Adjust margin on initial load and window resize
            adjustContentMargin();
            window.addEventListener("resize", adjustContentMargin);
        }
    });
    </script>
    """, unsafe_allow_html=True)
