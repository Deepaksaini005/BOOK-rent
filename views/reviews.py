import streamlit as st
from utils import get_session
from models import Review, Book

def show():
    st.title("⭐ My Reviews")

    if 'user' not in st.session_state or not st.session_state.user:
        st.error("Please login first")
        return

    session = get_session()
    user = st.session_state.user

    reviews = session.query(Review).filter_by(user_id=user.id).all()

    if reviews:
        for review in reviews:
            with st.expander(f"{review.book.title} - {review.rating}/5"):
                st.write(f"**Comment:** {review.comment}")
                st.write(f"**Date:** {review.created_at.strftime('%Y-%m-%d')}")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Edit Review", key=f"edit_{review.id}"):
                        st.session_state.edit_review = review
                        st.rerun()
                with col2:
                    if st.button("Delete Review", key=f"delete_{review.id}"):
                        session.delete(review)
                        session.commit()
                        st.success("Review deleted!")
                        st.rerun()
    else:
        st.write("You haven't written any reviews yet")

    # Edit review form
    if 'edit_review' in st.session_state:
        review = st.session_state.edit_review
        st.subheader(f"Edit Review for {review.book.title}")
        rating = st.slider("Rating", 1, 5, review.rating)
        comment = st.text_area("Comment", review.comment)
        if st.button("Update Review"):
            review.rating = rating
            review.comment = comment
            session.commit()
            st.success("Review updated!")
            del st.session_state.edit_review
            st.rerun()

    session.close()
