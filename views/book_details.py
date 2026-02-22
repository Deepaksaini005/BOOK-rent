import streamlit as st
from utils import get_session, calculate_rent_amount
from models import Book, Review, Rental, Payment
from datetime import datetime, timedelta, timezone

def show():
    if "selected_book" not in st.session_state:
        st.error("No book selected")
        return

    session = get_session()
    # Refresh book from DB for latest availability
    book_from_db = session.query(Book).filter_by(id=st.session_state.selected_book.id).first()
    if not book_from_db:
        st.error("Book not found")
        session.close()
        return
    book = book_from_db
    st.session_state.selected_book = book

    # Back button
    if st.button("← Back to list"):
        del st.session_state.selected_book
        st.rerun()

    st.title(f"📖 {book.title}")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("https://via.placeholder.com/300", caption=book.title)
    with col2:
        st.write(f"**Author:** {book.author}")
        st.write(f"**Genre:** {book.genre}")
        st.write(f"**Price per day:** ${book.price_per_day}")
        st.write(f"**Available copies:** {book.available}")
        st.write(f"**Description:** {book.description or 'No description available'}")

    # Rent form
    if 'user' in st.session_state and st.session_state.user:
        st.subheader("📅 Rent This Book")
        days = st.selectbox("Rental Duration", [7, 14, 30], index=0)
        total_amount = calculate_rent_amount(book, days)
        st.write(f"**Total Amount:** ${total_amount}")
        if st.button("Rent Now"):
            try:
                if book.available > 0:
                    rental = Rental(
                        user_id=st.session_state.user.id,
                        book_id=book.id,
                        due_date=datetime.now(timezone.utc) + timedelta(days=days),
                        total_amount=total_amount,
                    )
                    session.add(rental)
                    session.flush()
                    payment = Payment(rental_id=rental.id, amount=total_amount, status="completed")
                    session.add(payment)
                    book.available -= 1
                    session.commit()
                    st.success("Book rented successfully!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("Book not available")
            except Exception as e:
                session.rollback()
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please login to rent books")

    # Reviews
    st.subheader("⭐ Reviews")
    reviews = session.query(Review).filter_by(book_id=book.id).all()
    if reviews:
        for review in reviews:
            st.write(f"**{review.user.name}** ({review.rating}/5): {review.comment}")
    else:
        st.write("No reviews yet")

    # Add review
    if 'user' in st.session_state and st.session_state.user:
        st.subheader("Write a Review")
        rating = st.slider("Rating", 1, 5, 5)
        comment = st.text_area("Comment")
        if st.button("Submit Review"):
            review = Review(
                user_id=st.session_state.user.id,
                book_id=book.id,
                rating=rating,
                comment=comment
            )
            session.add(review)
            session.commit()
            st.success("Review submitted!")

    session.close()
