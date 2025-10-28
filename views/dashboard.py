import streamlit as st
from utils import get_session, calculate_late_fee
from models import Rental, Book
from datetime import datetime, timezone

def show():
    if 'user' not in st.session_state or not st.session_state.user:
        st.error("Please login first")
        return

    st.title("📊 Dashboard")

    session = get_session()
    user = st.session_state.user

    # Active rentals
    active_rentals = session.query(Rental).filter_by(user_id=user.id, status='active').all()
    st.subheader("📖 Active Rentals")
    if active_rentals:
        for rental in active_rentals:
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.write(f"**{rental.book.title}** by {rental.book.author}")
            with col2:
                st.write(f"Due: {rental.due_date.strftime('%Y-%m-%d')}")
            with col3:
                if st.button("Return", key=f"return_{rental.id}"):
                    rental.return_date = datetime.now(timezone.utc)
                    rental.status = 'returned'
                    rental.late_fee = calculate_late_fee(rental)
                    rental.book.available += 1
                    session.commit()
                    st.success("Book returned!")
                    st.rerun()
    else:
        st.write("No active rentals")

    # Recent activity
    st.subheader("📜 Recent Activity")
    recent_rentals = session.query(Rental).filter_by(user_id=user.id).order_by(Rental.rent_date.desc()).limit(5).all()
    for rental in recent_rentals:
        st.write(f"Rented **{rental.book.title}** on {rental.rent_date.strftime('%Y-%m-%d')}")

    session.close()
