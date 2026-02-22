import streamlit as st
from utils import get_session
from models import Wishlist, Book

def show():
    if "user" not in st.session_state or not st.session_state.user:
        st.error("Please login first")
        return

    st.markdown('<p class="main-header">❤️ My Wishlist</p>', unsafe_allow_html=True)
    st.markdown("Books you saved for later.")

    session = get_session()
    user = st.session_state.user

    wishlists = session.query(Wishlist).filter_by(user_id=user.id).all()

    if wishlists:
        st.caption(f"{len(wishlists)} book(s) in wishlist")
        cols = st.columns(3)
        for i, wishlist_item in enumerate(wishlists):
            book = wishlist_item.book
            with cols[i % 3]:
                st.image("https://via.placeholder.com/160x220/2d5a87/ffffff?text=Book", caption=book.title, use_container_width=True)
                st.write(f"**{book.title}**")
                st.caption(f"by {book.author} · ${book.price_per_day}/day")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("View", key=f"wish_details_{book.id}"):
                        st.session_state.selected_book = book
                        st.rerun()
                with col2:
                    if st.button("Remove", key=f"remove_wish_{wishlist_item.id}"):
                        try:
                            session.delete(wishlist_item)
                            session.commit()
                            st.success("Removed!")
                            st.rerun()
                        except Exception as e:
                            session.rollback()
                            st.error(f"Could not remove: {str(e)}")
    else:
        st.info("Your wishlist is empty. Add books from Search to get started.")

    session.close()
