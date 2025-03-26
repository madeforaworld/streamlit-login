# utils/firebase_auth.py

import pyrebase
from utils.firebase_config import firebase_config

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

def sign_in_with_email(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        return user
    except Exception as e:
        print("Login error:", e)
        return None

def sign_up_with_email(email, password):
    try:
        user = auth.create_user_with_email_and_password(email, password)
        return user
    except Exception as e:
        print("Signup error:", e)
        return None

