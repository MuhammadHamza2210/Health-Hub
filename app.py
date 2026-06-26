"""
Health Hub PRO — premium glassmorphism edition.
Run with:  streamlit run app.py
"""
import streamlit as st

from healthhub.config import APP_NAME, APP_ICON
from healthhub.styles import inject_theme
from healthhub.auth import (
    init_auth,
    load_users,
    logout_user,
    show_auth_page,
)
from healthhub.pages import dashboard, bmi, food, coach

st.set_page_config(page_title=APP_NAME, page_icon=APP_ICON,
                   layout="wide", initial_sidebar_state="expanded")

PAGES = ["Dashboard", "BMI Calculator", "Food Database", "AI Health Coach"]


def _go_to(page_name: str):
    st.session_state.nav = page_name
    st.rerun()


def main():
    inject_theme()
    init_auth()
    if not st.session_state.users:
        load_users()

    # --- Auth gate ---
    if not st.session_state.authenticated:
        show_auth_page()
        return

    user = st.session_state.users.get(st.session_state.current_user, {})
    user_name = user.get("name", "Friend")

    # --- One-time welcome celebration ---
    if st.session_state.get("show_welcome"):
        st.balloons()
        st.session_state.show_welcome = False

    # --- Sidebar: profile + navigation ---
    with st.sidebar:
        initial = (user_name[:1] or "?").upper()
        st.markdown(
            f"""
            <div class="glass" style="padding:18px;margin-bottom:14px;display:flex;
                 align-items:center;gap:14px;">
              <div style="width:48px;height:48px;border-radius:50%;display:flex;
                   align-items:center;justify-content:center;font-weight:700;color:#fff;
                   background:linear-gradient(135deg,#7c5cff,#ff6ec7);">{initial}</div>
              <div><div style="font-weight:700;">{user_name}</div>
                <div style="color:var(--muted);font-size:.82rem;">@{st.session_state.current_user}</div></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.session_state.setdefault("nav", "Dashboard")
        page = st.radio("Navigate", PAGES, index=PAGES.index(st.session_state.nav))
        st.session_state.nav = page

        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            logout_user()
            st.rerun()

    # --- Routing ---
    if page == "Dashboard":
        dashboard.render(user_name, _go_to)
    elif page == "BMI Calculator":
        bmi.render()
    elif page == "Food Database":
        food.render()
    elif page == "AI Health Coach":
        coach.render()


if __name__ == "__main__":
    main()
