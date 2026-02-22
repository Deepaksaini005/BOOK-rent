import streamlit as st
from utils import get_session, calculate_rent_amount
from models import Rental, Payment
from datetime import datetime, timedelta, timezone

def show():
    if "selected_book" not in st.session_state:
        st.error("No book selected")
        return

    if "user" not in st.session_state or not st.session_state.user:
        st.error("Please login first")
        return

    session = get_session()
    from models import Book
    book = session.query(Book).filter_by(id=st.session_state.selected_book.id).first()
    if not book:
        st.error("Book not found")
        session.close()
        return
    st.session_state.selected_book = book
    user = st.session_state.user

    if st.button("← Back"):
        if "selected_book" in st.session_state:
            del st.session_state.selected_book
        st.rerun()

    st.title(f"📅 Rent: {book.title}")
    st.caption(f"by {book.author}")

    days = st.selectbox("Select rental duration (days)", [7, 14, 30], format_func=lambda x: f"{x} days")
    total_amount = calculate_rent_amount(book, days)
    st.write(f"**Total:** ${total_amount:.2f}")

    st.subheader("💳 Payment (demo)")
    card_number = st.text_input("Card Number", type="password", placeholder="•••• •••• •••• ••••")
    expiry = st.text_input("Expiry (MM/YY)", placeholder="MM/YY")
    cvv = st.text_input("CVV", type="password", placeholder="•••")

    if st.button("Confirm Payment"):
        if not card_number or not expiry or not cvv:
            st.error("Please fill all payment fields.")
            session.close()
            return
        if book.available <= 0:
            st.error("This book is no longer available.")
            session.close()
            return

        try:
            rental = Rental(
                user_id=user.id,
                book_id=book.id,
                due_date=datetime.now(timezone.utc) + timedelta(days=days),
                total_amount=total_amount,
            )
            session.add(rental)
            session.flush()
            session.add(Payment(rental_id=rental.id, amount=total_amount, status="completed"))
            book.available -= 1
            session.commit()
            st.success("Payment successful! Book rented.")
            st.balloons()
            st.rerun()
        except Exception as e:
            session.rollback()
            st.error(f"An error occurred: {str(e)}")

    session.close()
