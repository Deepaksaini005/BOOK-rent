import streamlit as st
from utils import get_session
from models import Wishlist, Book

def show():
    if 'user' not in st.session_state or not st.session_state.user:
        st.error("Please login first")
        return

    st.title("❤️ My Wishlist")

    session = get_session()
    user = st.session_state.user

    wishlists = session.query(Wishlist).filter_by(user_id=user.id).all()

    if wishlists:
        cols = st.columns(3)
        for i, wishlist_item in enumerate(wishlists):
            book = wishlist_item.book
            with cols[i % 3]:
                st.image("https://via.placeholder.com/150", caption=book.title)
                st.write(f"**{book.title}** by {book.author}")
                st.write(f"Rent: ${book.price_per_day}/day")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("View Details", key=f"wish_details_{book.id}"):
                        st.session_state.selected_book = book
                        st.rerun()
                with col2:
                    if st.button("Remove", key=f"remove_wish_{wishlist_item.id}"):
                        session.delete(wishlist_item)
                        session.commit()
                        st.success("Removed from wishlist!")
                        st.rerun()
    else:
        st.write("Your wishlist is empty")

    session.close()
