import streamlit as st
import streamlit.components.v1 as components
from utils.firebase_auth import sign_in_with_email
import time

# Page config
st.set_page_config(page_title="Login", page_icon="🔐", layout="centered")

# Handle token from JS (Google login)
if "user" not in st.session_state:
    st.session_state["user"] = None

if st.session_state["user"]:
    st.success("Logged in successfully!")
    time.sleep(1)
    st.switch_page("Main_app.py")

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

    st.markdown('<div class="app-title">MindTag</div>', unsafe_allow_html=True)
    st.markdown('<div class="app-slogan">Extend your memory.</div>', unsafe_allow_html=True)

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

    # Google Sign-In via Embedded JS
    components.html(
        """
        <script src="https://www.gstatic.com/firebasejs/9.22.2/firebase-app-compat.js"></script>
        <script src="https://www.gstatic.com/firebasejs/9.22.2/firebase-auth-compat.js"></script>

        <div id="google-btn" style="
            background-color: #fff;
            border: 1px solid #ccc;
            border-radius: 10px;
            padding: 0.75rem;
            text-align: center;
            color: #444;
            cursor: pointer;
            font-weight: 500;
            margin-bottom: 1rem;
            width: 100%;
        ">Continue with Google</div>

        <script>
            const firebaseConfig = {
              apiKey: "AIzaSyDb-7VXzQb86XIJH-Q5Wlgf9ccNMMD3WCg",
              authDomain: "mindtag-ca61c.firebaseapp.com",
              projectId: "mindtag-ca61c",
              storageBucket: "mindtag-ca61c.appspot.com",
              messagingSenderId: "560275791939",
              appId: "1:560275791939:web:adea6051b949c3a3d474f6",
              measurementId: "G-BBL9E1DVQC"
            };

            firebase.initializeApp(firebaseConfig);

            const auth = firebase.auth();
            const provider = new firebase.auth.GoogleAuthProvider();

            document.getElementById("google-btn").onclick = function() {
                auth.signInWithPopup(provider)
                    .then((result) => {
                        const user = result.user;
                        const data = {
                            email: user.email,
                            name: user.displayName,
                            photo: user.photoURL,
                            uid: user.uid,
                            token: user.accessToken
                        };
                        window.parent.postMessage({ type: 'streamlit:setComponentValue', value: data }, '*');
                    })
                    .catch((error) => {
                        alert("Login failed: " + error.message);
                    });
            };
        </script>
        """,
        height=100,
    )

    st.markdown('<div class="footer-text">Don’t have an account? <a href="#">Sign up</a></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Listen for Google login result from JS
message = st.experimental_get_query_params()
if "_streamlit_component_value" in message:
    try:
        import json
        user = json.loads(message["_streamlit_component_value"][0])
        st.session_state["user"] = user
        st.rerun()
    except Exception as e:
        st.error("Failed to parse Google login data.")
