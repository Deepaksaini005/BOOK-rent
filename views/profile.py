import streamlit as st
from utils import get_session
from models import User

def show():
    if 'user' not in st.session_state or not st.session_state.user:
        st.error("Please login first")
        return

    st.title("👤 Profile")

    session = get_session()
    user = st.session_state.user

    with st.form("profile_form"):
        name = st.text_input("Full Name", user.name)
        email = st.text_input("Email", user.email)
        address = st.text_area("Address", user.address or "")
        phone = st.text_input("Phone", user.phone or "")

        if st.form_submit_button("Update Profile"):
            user.name = name
            user.email = email
            user.address = address
            user.phone = phone
            session.commit()
            st.success("Profile updated!")
            st.rerun()

    st.subheader("Change Password")
    with st.form("password_form"):
        current_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")

        if st.form_submit_button("Change Password"):
            if user.check_password(current_password):
                if new_password == confirm_password:
                    user.set_password(new_password)
                    session.commit()
                    st.success("Password changed!")
                else:
                    st.error("New passwords do not match")
            else:
                st.error("Current password is incorrect")

    session.close()
