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
        name = st.text_input("Full Name", placeholder="Your name").strip()
        email = st.text_input("Email", placeholder="you@example.com").strip()
        password = st.text_input("Password", type="password", placeholder="Min 6 characters")
        confirm_password = st.text_input("Confirm Password", type="password")

        if st.form_submit_button("Register"):
            if not name or not email or not password or not confirm_password:
                st.error("Please fill all fields.")
                return
            if not _is_valid_email(email):
                st.error("Please enter a valid email address.")
                return
            if len(password) < 6:
                st.error("Password must be at least 6 characters.")
                return
            if password != confirm_password:
                st.error("Passwords do not match.")
                return

            try:
                session = get_session()
                existing_user = session.query(User).filter_by(email=email).first()
                if existing_user:
                    st.error("This email is already registered.")
                else:
                    user = User(name=name, email=email)
                    user.set_password(password)
                    session.add(user)
                    session.commit()
                    st.success("Registration successful! Please login.")
                    session.close()
                    st.rerun()
                session.close()
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
