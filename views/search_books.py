import streamlit as st
from utils import get_session
from models import Book, Wishlist

def show():
    st.title("🔍 Search Books")

    session = get_session()

    # Search and filters
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        search_query = st.text_input("Search by title or author")
    with col2:
        genres = session.query(Book.genre).distinct().filter(Book.genre.isnot(None)).all()
        genre_list = ["All"] + [g[0] for g in genres]
        genre_filter = st.selectbox("Genre", genre_list)
    with col3:
        sort_by = st.selectbox("Sort by", ["Title", "Author", "Price"])

    # Query books
    query = session.query(Book)
    if search_query:
        query = query.filter(Book.title.ilike(f"%{search_query}%") | Book.author.ilike(f"%{search_query}%"))
    if genre_filter != "All":
        query = query.filter_by(genre=genre_filter)
    if sort_by == "Title":
        query = query.order_by(Book.title)
    elif sort_by == "Author":
        query = query.order_by(Book.author)
    elif sort_by == "Price":
        query = query.order_by(Book.price_per_day)

    books = query.all()

    # Display books
    if books:
        cols = st.columns(3)
        for i, book in enumerate(books):
            with cols[i % 3]:
                st.image("https://via.placeholder.com/150", caption=book.title)
                st.write(f"**{book.title}**")
                st.write(f"by {book.author}")
                st.write(f"Genre: {book.genre}")
                st.write(f"Rent: ${book.price_per_day}/day")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("View Details", key=f"details_{book.id}"):
                        st.session_state.selected_book = book
                        st.rerun()
                with col2:
                    if 'user' in st.session_state and st.session_state.user:
                        existing_wishlist = session.query(Wishlist).filter_by(user_id=st.session_state.user.id, book_id=book.id).first()
                        if existing_wishlist:
                            st.write("Already in wishlist")
                        else:
                            if st.button("Add to Wishlist", key=f"wishlist_{book.id}"):
                                wishlist_item = Wishlist(user_id=st.session_state.user.id, book_id=book.id)
                                session.add(wishlist_item)
                                session.commit()
                                st.success("Added to wishlist!")
                                st.rerun()
                    else:
                        st.write("Login to add to wishlist")
    else:
        st.write("No books found")

    session.close()
