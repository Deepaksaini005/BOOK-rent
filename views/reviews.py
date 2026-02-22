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
                st.write(f"**Comment:** {review.comment or '(No comment)'}")
                st.write(f"**Date:** {review.created_at.strftime('%Y-%m-%d')}")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Edit Review", key=f"edit_{review.id}"):
                        st.session_state.edit_review = review
                        st.rerun()
                with col2:
                    if st.button("Delete Review", key=f"delete_{review.id}"):
                        try:
                            session.delete(review)
                            session.commit()
                            st.success("Review deleted!")
                            st.rerun()
                        except Exception as e:
                            session.rollback()
                            st.error(f"Could not delete: {str(e)}")
    else:
        st.write("You haven't written any reviews yet")

    # Edit review form
    if "edit_review" in st.session_state:
        review = st.session_state.edit_review
        db_review = session.query(Review).filter_by(id=review.id).first()
        if not db_review:
            del st.session_state.edit_review
            st.rerun()
        else:
            st.subheader(f"Edit Review for {db_review.book.title}")
            rating = st.slider("Rating", 1, 5, db_review.rating)
            comment = st.text_area("Comment", db_review.comment or "")
            if st.button("Update Review"):
                try:
                    db_review.rating = rating
                    db_review.comment = (comment or "").strip() or None
                    session.commit()
                    st.success("Review updated!")
                    del st.session_state.edit_review
                    st.rerun()
                except Exception as e:
                    session.rollback()
                    st.error(f"Could not update: {str(e)}")

    session.close()
