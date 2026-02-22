import streamlit as st
from utils import get_session, get_recommendations
from models import Book

def show():
    st.markdown('<p class="main-header">📚 Welcome to Book Rental App</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Discover, rent, and enjoy your favorite books. No commitment — pay per day.</p>', unsafe_allow_html=True)

    session = get_session()

    # Hero stats (quick counts)
    total_books = session.query(Book).count()
    available = session.query(Book).filter(Book.available > 0).count()
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Books to Rent", total_books)
    with c2:
        st.metric("Available Now", available)
    with c3:
        st.metric("Genres", session.query(Book.genre).distinct().count())

    st.markdown("---")
    st.subheader("🔥 Trending Books")
    trending_books = session.query(Book).limit(6).all()
    cols = st.columns(3)
    for i, book in enumerate(trending_books):
        with cols[i % 3]:
            st.image("https://via.placeholder.com/160x220/1e3a5f/ffffff?text=Book", caption=book.title, use_container_width=True)
            st.write(f"**{book.title}**")
            st.caption(f"by {book.author}")
            st.write(f"*{book.genre or 'General'}* · ${book.price_per_day}/day")
            if st.button("View Details", key=f"trend_{book.id}"):
                st.session_state.selected_book = book
                st.rerun()

    if "user" in st.session_state and st.session_state.user:
        st.markdown("---")
        st.subheader("🤖 Recommended for You")
        recommendations = get_recommendations(st.session_state.user.id, session)
        if recommendations:
            cols = st.columns(3)
            for i, book in enumerate(recommendations):
                with cols[i % 3]:
                    st.image("https://via.placeholder.com/160x220/2d5a87/ffffff?text=Book", caption=book.title, use_container_width=True)
                    st.write(f"**{book.title}**")
                    st.caption(f"by {book.author}")
                    if st.button("View & Rent", key=f"rec_{book.id}"):
                        st.session_state.selected_book = book
                        st.rerun()
        else:
            st.info("Rent a few books to get personalized recommendations.")

    session.close()
