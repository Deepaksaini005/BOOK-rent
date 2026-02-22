import streamlit as st
import re
from utils import get_session
from models import User

def _is_valid_email(email):
    return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", (email or "").strip()))

def show():
    st.markdown('<p class="main-header">🔐 Login</p>', unsafe_allow_html=True)
    st.markdown("Enter your credentials to access your account.")

    with st.form("login_form"):
        email = st.text_input("Email", placeholder="you@example.com").strip()
        password = st.text_input("Password", type="password", placeholder="••••••••")

        if st.form_submit_button("Login"):
            if not email or not password:
                st.error("Please fill all fields.")
                return
            if not _is_valid_email(email):
                st.error("Please enter a valid email address.")
                return

            try:
                session = get_session()
                try:
                    user = session.query(User).filter_by(email=email).first()
                    if user and user.check_password(password):
                        st.session_state.user = user
                        st.success("Login successful! Welcome back.")
                        st.rerun()
                    else:
                        st.error("Invalid email or password.")
                finally:
                    session.close()
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
