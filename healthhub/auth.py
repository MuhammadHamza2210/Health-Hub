"""User authentication: hashing, persistence and the premium login page."""
import hashlib
import json
import time
from datetime import datetime

import streamlit as st

from healthhub.config import USERS_FILE
from healthhub.styles import hero


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(stored: str, provided: str) -> bool:
    return stored == hashlib.sha256(provided.encode()).hexdigest()


def init_auth() -> None:
    st.session_state.setdefault("users", {})
    st.session_state.setdefault("authenticated", False)
    st.session_state.setdefault("current_user", None)
    st.session_state.setdefault("show_welcome", False)


def save_users() -> None:
    try:
        with open(USERS_FILE, "w") as f:
            json.dump(st.session_state.users, f)
    except Exception:
        pass


def load_users() -> None:
    try:
        with open(USERS_FILE, "r") as f:
            st.session_state.users = json.load(f)
    except Exception:
        st.session_state.users = {}


def register_user(username, password, email, name):
    if not all([username, password, name]):
        return False, "Please fill in name, username and password."
    if username in st.session_state.users:
        return False, "Username already exists."
    st.session_state.users[username] = {
        "password": hash_password(password),
        "email": email,
        "name": name,
        "created_at": datetime.now().timestamp(),
        "last_login": None,
        "profile": {"age": None, "height": None, "weight": None, "goals": None},
    }
    save_users()
    return True, "Registration successful"


def login_user(username, password):
    if username not in st.session_state.users:
        return False, "Username not found."
    if not verify_password(st.session_state.users[username]["password"], password):
        return False, "Incorrect password."
    st.session_state.users[username]["last_login"] = datetime.now().timestamp()
    st.session_state.authenticated = True
    st.session_state.current_user = username
    st.session_state.show_welcome = True
    save_users()
    return True, "Login successful"


def logout_user():
    st.session_state.authenticated = False
    st.session_state.current_user = None


def show_auth_page() -> None:
    """Premium glassmorphism login / signup screen."""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        hero(
            "Health Hub PRO",
            "Your personal health & wellness companion — reimagined.",
            pill="💎 Premium Edition",
        )
        with st.container():
            st.markdown('<div class="glass">', unsafe_allow_html=True)
            tab_login, tab_signup = st.tabs(["🔓  Login", "✨  Create Account"])

            with tab_login:
                with st.form("login_form"):
                    st.markdown("#### Welcome back")
                    username = st.text_input("Username", key="login_username")
                    password = st.text_input("Password", type="password", key="login_password")
                    if st.form_submit_button("Login", use_container_width=True):
                        ok, msg = login_user(username, password)
                        if ok:
                            st.success(msg)
                            time.sleep(0.6)
                            st.rerun()
                        else:
                            st.error(msg)

            with tab_signup:
                with st.form("signup_form"):
                    st.markdown("#### Join the community")
                    name = st.text_input("Full Name", key="signup_name")
                    email = st.text_input("Email", key="signup_email")
                    username = st.text_input("Username", key="signup_username")
                    password = st.text_input("Password", type="password", key="signup_password")
                    confirm = st.text_input("Confirm Password", type="password", key="signup_confirm")
                    if st.form_submit_button("Create Account", use_container_width=True):
                        if password != confirm:
                            st.error("Passwords don't match.")
                        else:
                            ok, msg = register_user(username, password, email, name)
                            if ok:
                                st.success(msg)
                                st.session_state.authenticated = True
                                st.session_state.current_user = username
                                st.session_state.show_welcome = True
                                time.sleep(0.6)
                                st.rerun()
                            else:
                                st.error(msg)
            st.markdown("</div>", unsafe_allow_html=True)
