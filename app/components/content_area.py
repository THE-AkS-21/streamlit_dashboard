from turtle import st

st.markdown("""
        <style>
        .custom-content {
            margin-top: 50px;
            margin-left: 70px;
            padding: 20px;
            transition: margin-left 0.3s ease;
        }
        .custom-sidebar:hover ~ .custom-content {
            margin-left: 220px;
        }
        @media screen and (max-width: 768px) {
            .custom-content {
                margin-left: 0;
            }
        }
        </style>
        <div class="custom-content">
    """, unsafe_allow_html=True)