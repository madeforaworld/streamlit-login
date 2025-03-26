import streamlit as st

# Set page config
st.set_page_config(page_title="Login", page_icon="🔐", layout="centered")

# Custom CSS for UI3 Light Design
st.markdown("""
    <style>
        html, body, [data-testid="stApp"] {
            background-color: #f5f7fa !important;
        }

        .login-container {
            max-width: 400px;
            margin: 5vh auto;
            background-color: #ffffff;
            padding: 3rem 2.5rem;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
        }

        .login-header {
            text-align: center;
            font-size: 1.8rem;
            font-weight: 600;
            color: #222;
            margin-bottom: 1.5rem;
        }

        .stTextInput > div > div > input {
            background-color: #f9fafb;
            padding: 0.75rem;
            border-radius: 10px;
            border: 1px solid #ddd;
            color: #111;
        }

        .stButton > button {
            background-color: #3366FF;
            color: white;
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: 12px;
            font-weight: 600;
            width: 100%;
            margin-top: 1rem;
            transition: 0.3s ease;
        }

        .stButton > button:hover {
            background-color: #254eda;
        }

        .divider {
            text-align: center;
            margin: 1.5rem 0;
            color: #999;
        }

        .google-btn {
            background-color: #fff;
            border: 1px solid #ccc;
            border-radius: 10px;
            padding: 0.75rem;
            text-align: center;
            color: #444;
            cursor: pointer;
            font-weight: 500;
            margin-bottom: 1rem;
        }

        .footer-text {
            text-align: center;
            font-size: 0.9rem;
            color: #666;
            margin-top: 1rem;
        }

        .footer-text a {
            color: #3366FF;
            text-decoration: none;
            font-weight: 500;
        }

        .footer-text a:hover {
            text-decoration: underline;
        }
    </style>
""", unsafe_allow_html=True)

# Layout
with st.container():
    st.markdown('<div class="login-container">', unsafe_allow_html=True)

    st.markdown('<div class="login-header">Welcome back 👋</div>', unsafe_allow_html=True)

    email = st.text_input("Email", placeholder="you@example.com")
    password = st.text_input("Password", type="password", placeholder="••••••••")

    if st.button("Sign In"):
        if email and password:
            st.success("Logged in successfully!")
        else:
            st.warning("Please enter your email and password.")

    st.markdown('<div class="divider">— or —</div>', unsafe_allow_html=True)

    st.markdown('<div class="google-btn">Continue with Google</div>', unsafe_allow_html=True)

    st.markdown('<div class="footer-text">Don’t have an account? <a href="#">Sign up</a></div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
