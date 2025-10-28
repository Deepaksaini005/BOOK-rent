import streamlit as st
from utils import get_session
from models import User

def show():
    st.title("📝 Register")

    name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if not name or not email or not password or not confirm_password:
            st.error("Please fill all fields")
            return

        if password != confirm_password:
            st.error("Passwords do not match")
            return

        try:
            session = get_session()
            existing_user = session.query(User).filter_by(email=email).first()
            if existing_user:
                st.error("Email already registered")
            else:
                user = User(name=name, email=email)
                user.set_password(password)
                session.add(user)
                session.commit()
                st.success("Registration successful! Please login.")
                st.rerun()
            session.close()
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
