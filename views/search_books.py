import streamlit as st
from utils import get_session
from models import Book, Wishlist

def show():
    st.markdown('<p class="main-header">🔍 Search Books</p>', unsafe_allow_html=True)
    st.markdown("Filter by title, author, or genre and sort the results.")

    session = get_session()

    # Search and filters
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        search_query = st.text_input("Search by title or author", placeholder="Type to search...").strip()
    with col2:
        genres = [g[0] for g in session.query(Book.genre).distinct().filter(Book.genre.isnot(None)).order_by(Book.genre).all()]
        genre_list = ["All"] + genres
        genre_filter = st.selectbox("Genre", genre_list)
    with col3:
        sort_by = st.selectbox("Sort by", ["Title", "Author", "Price (low first)"])

    # Query books
    query = session.query(Book)
    if search_query:
        query = query.filter(
            Book.title.ilike(f"%{search_query}%") | Book.author.ilike(f"%{search_query}%")
        )
    if genre_filter != "All":
        query = query.filter_by(genre=genre_filter)
    if sort_by == "Title":
        query = query.order_by(Book.title)
    elif sort_by == "Author":
        query = query.order_by(Book.author)
    else:
        query = query.order_by(Book.price_per_day)

    books = query.all()

    if books:
        st.caption(f"Found {len(books)} book(s)")
        cols = st.columns(3)
        for i, book in enumerate(books):
            with cols[i % 3]:
                st.image("https://via.placeholder.com/160x220/1e3a5f/ffffff?text=Book", caption=book.title, use_container_width=True)
                st.write(f"**{book.title}**")
                st.caption(f"by {book.author}")
                st.write(f"*{book.genre or 'General'}* · ${book.price_per_day}/day")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("View Details", key=f"details_{book.id}"):
                        st.session_state.selected_book = book
                        st.rerun()
                with col2:
                    if "user" in st.session_state and st.session_state.user:
                        existing_wishlist = session.query(Wishlist).filter_by(
                            user_id=st.session_state.user.id, book_id=book.id
                        ).first()
                        if existing_wishlist:
                            st.caption("✓ In wishlist")
                        else:
                            if st.button("❤️ Wishlist", key=f"wishlist_{book.id}"):
                                try:
                                    session.add(Wishlist(user_id=st.session_state.user.id, book_id=book.id))
                                    session.commit()
                                    st.success("Added to wishlist!")
                                    st.rerun()
                                except Exception as e:
                                    session.rollback()
                                    st.error(f"Could not add to wishlist: {str(e)}")
                    else:
                        st.caption("Login to add")
    else:
        st.info("No books found. Try changing filters or search term.")

    session.close()
