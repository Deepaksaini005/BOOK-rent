import streamlit as st
from utils import get_session, get_recommendations
from models import Book

def show():
    st.title("📚 Welcome to Book Rental App")
    st.markdown("Discover, rent, and enjoy your favorite books!")

    session = get_session()

    # Featured books
    st.subheader("🔥 Trending Books")
    trending_books = session.query(Book).limit(6).all()
    cols = st.columns(3)
    for i, book in enumerate(trending_books):
        with cols[i % 3]:
            st.image("https://via.placeholder.com/150", caption=book.title)
            st.write(f"**{book.title}** by {book.author}")
            st.write(f"Genre: {book.genre}")
            st.write(f"Rent: ${book.price_per_day}/day")
            if st.button(f"View Details {book.id}", key=f"trend_{book.id}"):
                st.session_state.selected_book = book
                st.rerun()

    # Recommendations
    if 'user' in st.session_state and st.session_state.user:
        st.subheader("🤖 Recommended for You")
        recommendations = get_recommendations(st.session_state.user.id, session)
        cols = st.columns(3)
        for i, book in enumerate(recommendations):
            with cols[i % 3]:
                st.image("https://via.placeholder.com/150", caption=book.title)
                st.write(f"**{book.title}** by {book.author}")
                if st.button(f"Rent Now {book.id}", key=f"rec_{book.id}"):
                    st.session_state.selected_book = book
                    st.rerun()

    session.close()
