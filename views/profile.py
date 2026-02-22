import streamlit as st
from utils import get_session
from models import User
def show():
    if "user" not in st.session_state or not st.session_state.user:
        st.error("Please login first")
        return

    st.title("👤 Profile")

    session = get_session()
    user = st.session_state.user

    try:
        with st.form("profile_form"):
            name = st.text_input("Full Name", user.name or "")
            email = st.text_input("Email", user.email or "")
            address = st.text_area("Address", user.address or "")
            phone = st.text_input("Phone", user.phone or "")

            if st.form_submit_button("Update Profile"):
                db_user = session.query(User).filter_by(id=user.id).first()
                if not db_user:
                    st.error("Session expired. Please login again.")
                else:
                    other = session.query(User).filter_by(email=email.strip()).first()
                    if other and other.id != user.id:
                        st.error("This email is already used by another account.")
                    else:
                        db_user.name = name.strip() or db_user.name
                        db_user.email = email.strip()
                        db_user.address = address.strip() or None
                        db_user.phone = phone.strip() or None
                        session.commit()
                        st.session_state.user = db_user
                        st.success("Profile updated!")
                        st.rerun()

        st.subheader("Change Password")
        with st.form("password_form"):
            current_password = st.text_input("Current Password", type="password")
            new_password = st.text_input("New Password", type="password")
            confirm_password = st.text_input("Confirm New Password", type="password")

            if st.form_submit_button("Change Password"):
                db_user = session.query(User).filter_by(id=user.id).first()
                if not db_user:
                    st.error("Session expired. Please login again.")
                elif db_user.check_password(current_password):
                    if new_password == confirm_password:
                        if len(new_password) < 6:
                            st.error("New password must be at least 6 characters")
                        else:
                            db_user.set_password(new_password)
                            session.commit()
                            st.session_state.user = db_user
                            st.success("Password changed!")
                    else:
                        st.error("New passwords do not match")
                else:
                    st.error("Current password is incorrect")
    finally:
        session.close()
