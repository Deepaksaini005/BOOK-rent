import streamlit as st
from utils import get_session, calculate_late_fee, generate_invoice
from models import Rental
from datetime import datetime, timezone

def show():
    if 'user' not in st.session_state or not st.session_state.user:
        st.error("Please login first")
        return

    st.title("📖 My Rentals")

    session = get_session()
    user = st.session_state.user

    rentals = session.query(Rental).filter_by(user_id=user.id).order_by(Rental.rent_date.desc()).all()

    for rental in rentals:
        with st.expander(f"{rental.book.title} - {rental.status}"):
            st.write(f"**Author:** {rental.book.author}")
            st.write(f"**Rent Date:** {rental.rent_date.strftime('%Y-%m-%d')}")
            st.write(f"**Due Date:** {rental.due_date.strftime('%Y-%m-%d')}")
            st.write(f"**Total Amount:** ${rental.total_amount}")
            if rental.return_date:
                st.write(f"**Return Date:** {rental.return_date.strftime('%Y-%m-%d')}")
                late_fee = calculate_late_fee(rental)
                if late_fee > 0:
                    st.write(f"**Late Fee:** ${late_fee}")
            if rental.status == 'active':
                if st.button("Return Book", key=f"return_{rental.id}"):
                    rental.return_date = datetime.now(timezone.utc)
                    rental.status = 'returned'
                    rental.late_fee = calculate_late_fee(rental)
                    rental.book.available += 1
                    session.commit()
                    st.success("Book returned!")
                    st.rerun()
            if st.button("Download Invoice", key=f"invoice_{rental.id}"):
                try:
                    filename = generate_invoice(rental)
                    with open(filename, "rb") as f:
                        st.download_button("Download", f, file_name=filename, key=f"download_{rental.id}")
                except Exception as e:
                    st.error(f"Error generating invoice: {str(e)}")

    session.close()
