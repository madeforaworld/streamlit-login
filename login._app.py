import streamlit as st
from utils.firebase_auth import sign_in_with_email
import time

# Page config
st.set_page_config(page_title="Login", page_icon="🔐", layout="centered")

# Custom CSS
st.markdown("""
    <style>
        html, body, [data-testid="stApp"] {
            background-color: #f5f7fa !important;
            padding-top: 0 !important;
        }

        [data-testid="stVerticalBlock"] {
            padding-top: 0 !important;
            margin-top: 0 !important;
        }

        .login-container {
            max-width: 400px;
            margin: 3vh auto 5vh auto;
            background-color: #ffffff;
            padding: 2.5rem 2rem;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
        }

        .app-title {
            text-align: center;
            font-size: 2.2rem;
            font-weight: 700;
            color: #222;
            margin-bottom: 0.25rem;
        }

        .app-slogan {
            text-align: center;
            font-size: 1.1rem;
            color: #666;
            margin-bottom: 2rem;
        }

        .stTextInput > div > div > input {
            background-color: #f9fafb !important;
            padding: 0.75rem;
            border-radius: 10px;
            border: 1px solid #ddd !important;
            color: #111;
            box-shadow: none !important;
            outline: none !important;
            filter: none !important;
            transition: border 0.2s ease-in-out;
        }

        .stTextInput > div > div > input:focus {
            border: 1px solid #3366FF !important;
        }

        .stButton > button {
            background-color: #3366FF !important;
            color: white !important;
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: 12px;
            font-weight: 600;
            width: 100%;
            margin-top: 1rem;
            transition: background-color 0.3s ease;
            box-shadow: none !important;
        }

        .stButton > button:hover {
            background-color: #254eda !important;
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

        .google-btn:hover {
            background-color: #f1f1f1;
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

# Check for login token (optional future step)
query_params = st.query_params
if "user" in st.session_state:
    st.switch_page("Main_app.py")

# Layout
with st.container():
    st.markdown('<div class="login-container">', unsafe_allow_html=True)

    st.markdown('<div class="app-title">MindTag</div>', unsafe_allow_html=True)
    st.markdown('<div class="app-slogan">Extend your memory.</div>', unsafe_allow_html=True)

    # Email login
    email = st.text_input("Email", placeholder="you@example.com")
    password = st.text_input("Password", type="password", placeholder="••••••••")

    if st.button("Sign In"):
        if email and password:
            with st.spinner("Authenticating..."):
                result = sign_in_with_email(email, password)
                if isinstance(result, dict) and "error" in result:
                    st.error("Login failed: " + result["error"])
                else:
                    st.session_state["user"] = result
                    st.success("Login successful! Redirecting...")
                    time.sleep(1)
                    st.switch_page("Main_app.py")
        else:
            st.warning("Please enter your email and password.")

    st.markdown('<div class="divider">— or —</div>', unsafe_allow_html=True)

    # Google Login via redirect to Firebase hosted page
    redirect_url = "https://mindtag-ca61c.firebaseapp.com/__/auth/handler?continueUrl=https://app-app-moxethh5kyo8vbmchd5mrs.streamlit.app"

    st.markdown(f"""
        <a href="{redirect_url}" target="_self">
            <div class="google-btn">Continue with Google</div>
        </a>
    """, unsafe_allow_html=True)

    st.markdown('<div class="footer-text">Don’t have an account? <a href="#">Sign up</a></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
