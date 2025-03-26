import streamlit as st

# Page setup
st.set_page_config(page_title="Login", page_icon="🔐", layout="centered")

# Custom CSS to style UI3 vibes
st.markdown("""
    <style>
        .login-card {
            background-color: white;
            padding: 3rem 2rem;
            border-radius: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            width: 100%;
            max-width: 400px;
            margin: auto;
        }
        .login-header {
            font-size: 1.8rem;
            font-weight: 600;
            margin-bottom: 1.5rem;
            text-align: center;
        }
        .login-footer {
            text-align: center;
            margin-top: 1rem;
            font-size: 0.9rem;
            color: #888;
        }
        .or-divider {
            text-align: center;
            margin: 1rem 0;
            color: #999;
        }
        .google-btn {
            background-color: #fff;
            border: 1px solid #ccc;
            border-radius: 10px;
            padding: 0.5rem 1rem;
            width: 100%;
            text-align: center;
            cursor: pointer;
            margin-bottom: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# Layout container
with st.container():
    st.markdown('<div class="login-card">', unsafe_allow_html=True)

    st.markdown('<div class="login-header">Welcome back 👋</div>', unsafe_allow_html=True)

    email = st.text_input("Email", placeholder="you@example.com")
    password = st.text_input("Password", type="password", placeholder="••••••••")

    if st.button("Sign In"):
        if email and password:
            st.success("Logged in successfully!")
        else:
            st.warning("Please fill in both fields.")

    st.markdown('<div class="or-divider">— or —</div>', unsafe_allow_html=True)

    st.markdown('<div class="google-btn">Continue with Google</div>', unsafe_allow_html=True)

    st.markdown('<div class="login-footer">Don’t have an account? <a href="#">Sign up</a></div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
