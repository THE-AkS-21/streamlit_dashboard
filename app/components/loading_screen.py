import streamlit as st

def loading_screen():
    st.markdown("""
        <style>
            /* Overlay container */
            #loading-overlay {
                position: fixed;
                inset: 0;
                background-color: #ffffff;
                z-index: 9999;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                font-family: 'Segoe UI', Roboto, monospace;
                font-weight: 600;
                letter-spacing: 1.2px;
                text-align: center;
            }

            /* Loading text */
            #loading-text {
                font-size: 2.5rem;
                color: #1f2937;
                margin-bottom: 2rem;
            }

            .animate-blink {
                animation: blink 1s step-end infinite;
                color: #374151;
            }

            @keyframes blink {
                50% { opacity: 0; }
            }

            /* Progress bar container */
            .loading-bar-container {
                width: 240px;
                height: 6px;
                border-radius: 6px;
                background: #e5e7eb;
                overflow: hidden;
                box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
            }

            .loading-bar {
                height: 100%;
                width: 40%;
                background-color: #3b82f6;
                animation: loading-bar 1.5s infinite ease-in-out;
                box-shadow: 0 0 8px #3b82f6;
            }

            @keyframes loading-bar {
                0% { transform: translateX(-100%); }
                50% { transform: translateX(100%); }
                100% { transform: translateX(100%); }
            }

            /* Optional: Blur background (disable if not needed) */
            /* body::before {
                content: "";
                position: fixed;
                inset: 0;
                backdrop-filter: blur(4px);
                z-index: 9998;
            } */
        </style>

        <div id="loading-overlay">
            <div id="loading-text">|</div>
            <div class="loading-bar-container">
                <div class="loading-bar"></div>
            </div>
        </div>

        <script>
            const fullText = "BOMBAY SHAVING COMPANY  |  Loading...";
            let index = 0;

            const interval = setInterval(() => {
                const text = fullText.substring(0, index);
                document.getElementById("loading-text").innerHTML = text + '<span class="animate-blink">|</span>';
                index++;

                if (index > fullText.length) {
                    clearInterval(interval);
                    setTimeout(() => {
                        const overlay = document.getElementById("loading-overlay");
                        if (overlay) overlay.style.display = "none";
                    }, 600);
                }
            }, 100);
        </script>
    """, unsafe_allow_html=True)
