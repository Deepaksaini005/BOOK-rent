import streamlit as st
from utils import get_session
from models import User

def show():
    st.title("🔐 Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if not email or not password:
            st.error("Please fill all fields")
            return

        try:
            session = get_session()
            user = session.query(User).filter_by(email=email).first()
            if user and user.check_password(password):
                st.session_state.user = user
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid email or password")
            session.close()
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
