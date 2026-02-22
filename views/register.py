import streamlit as st
import re
from utils import get_session
from models import User

def _is_valid_email(email):
    return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", (email or "").strip()))

def show():
    st.markdown('<p class="main-header">📝 Create Account</p>', unsafe_allow_html=True)
    st.markdown("Join us to rent books and manage your reading list.")

    with st.form("register_form"):
        name = st.text_input("Full Name", placeholder="Your name")
        email = st.text_input("Email", placeholder="you@example.com")
        password = st.text_input("Password", type="password", placeholder="Min 6 characters")
        confirm_password = st.text_input("Confirm Password", type="password")

        if st.form_submit_button("Register"):
            name = (name or "").strip()
            email = (email or "").strip()

            if not name:
                st.error("Please enter your name.")
            elif not email:
                st.error("Please enter your email.")
            elif not password:
                st.error("Please enter a password.")
            elif not confirm_password:
                st.error("Please confirm your password.")
            elif not _is_valid_email(email):
                st.error("Please enter a valid email address (e.g. name@example.com).")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters.")
            elif password != confirm_password:
                st.error("Passwords do not match.")
            else:
                try:
                    session = get_session()
                    try:
                        existing_user = session.query(User).filter_by(email=email).first()
                        if existing_user:
                            st.error("This email is already registered. Try logging in.")
                        else:
                            user = User(name=name, email=email)
                            user.set_password(password)
                            session.add(user)
                            session.commit()
                            st.success("Account created! Redirecting to login...")
                            st.session_state.nav_radio = "Login"
                            st.rerun()
                    finally:
                        session.close()
                except Exception as e:
                    st.error(f"Registration failed: {str(e)}")
