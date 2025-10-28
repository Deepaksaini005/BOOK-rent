import streamlit as st
from utils import get_session, calculate_rent_amount
from models import Rental, Payment
from datetime import datetime, timedelta, timezone

def show():
    if 'selected_book' not in st.session_state:
        st.error("No book selected")
        return

    if 'user' not in st.session_state or not st.session_state.user:
        st.error("Please login first")
        return

    book = st.session_state.selected_book
    user = st.session_state.user
    session = get_session()

    st.title(f"📅 Rent {book.title}")

    days = st.selectbox("Select rental duration", [7, 14, 30])
    total_amount = calculate_rent_amount(book, days)
    st.write(f"**Total Amount:** ${total_amount}")

    # Mock payment
    st.subheader("💳 Payment")
    card_number = st.text_input("Card Number", type="password")
    expiry = st.text_input("Expiry (MM/YY)")
    cvv = st.text_input("CVV", type="password")

    if st.button("Confirm Payment"):
        if not card_number or not expiry or not cvv:
            st.error("Please fill payment details")
            return

        try:
            # Create rental
            rental = Rental(
                user_id=user.id,
                book_id=book.id,
                due_date=datetime.now(timezone.utc) + timedelta(days=days),
                total_amount=total_amount
            )
            book.available -= 1
            session.add(rental)
            session.commit()

            # Create payment
            payment = Payment(rental_id=rental.id, amount=total_amount, status='completed')
            session.add(payment)
            session.commit()

            st.success("Payment successful! Book rented.")
            st.balloons()
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

    session.close()
