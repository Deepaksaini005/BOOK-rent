import streamlit as st
from utils import get_session, get_analytics, create_charts
from models import User, Book, Rental, Payment

def show():
    if 'user' not in st.session_state or st.session_state.user.role != 'admin':
        st.error("Access denied")
        return

    st.title("🧑‍💼 Admin Dashboard")

    session = get_session()

    # Analytics
    analytics = get_analytics()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Users", analytics['total_users'])
    with col2:
        st.metric("Total Books", analytics['total_books'])
    with col3:
        st.metric("Active Rentals", analytics['active_rentals'])
    with col4:
        st.metric("Total Revenue", f"${analytics['total_revenue']:.2f}")

    # Charts
    st.subheader("📊 Analytics")
    fig = create_charts()
    st.plotly_chart(fig)

    # Manage Books
    st.subheader("📚 Manage Books")
    if st.button("Add New Book"):
        st.session_state.add_book = True
    if 'add_book' in st.session_state and st.session_state.add_book:
        with st.form("add_book_form"):
            title = st.text_input("Title")
            author = st.text_input("Author")
            genre = st.text_input("Genre")
            price = st.number_input("Price per day", min_value=0.0)
            stock = st.number_input("Stock", min_value=1)
            description = st.text_area("Description")
            if st.form_submit_button("Add Book"):
                book = Book(title=title, author=author, genre=genre, price_per_day=price, stock=stock, available=stock, description=description)
                session.add(book)
                session.commit()
                st.success("Book added!")
                st.session_state.add_book = False
                st.rerun()

    # Edit book form
    if 'edit_book' in st.session_state:
        book = st.session_state.edit_book
        st.subheader(f"Edit Book: {book.title}")
        with st.form("edit_book_form"):
            title = st.text_input("Title", book.title)
            author = st.text_input("Author", book.author)
            genre = st.text_input("Genre", book.genre)
            price = st.number_input("Price per day", min_value=0.0, value=book.price_per_day)
            stock = st.number_input("Stock", min_value=1, value=book.stock)
            description = st.text_area("Description", book.description or "")
            if st.form_submit_button("Update Book"):
                book.title = title
                book.author = author
                book.genre = genre
                book.price_per_day = price
                book.stock = stock
                book.available = min(book.available, stock)  # Adjust available if stock decreased
                book.description = description
                session.commit()
                st.success("Book updated!")
                del st.session_state.edit_book
                st.rerun()

    # List books
    books = session.query(Book).all()
    for book in books:
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
        with col1:
            st.write(f"**{book.title}** by {book.author}")
        with col2:
            st.write(f"Stock: {book.stock}")
        with col3:
            if st.button("Edit", key=f"edit_{book.id}"):
                st.session_state.edit_book = book
                st.rerun()
        with col4:
            if st.button("Delete", key=f"delete_{book.id}"):
                session.delete(book)
                session.commit()
                st.success("Book deleted!")
                st.rerun()

    # Manage Users
    st.subheader("👥 Manage Users")
    users = session.query(User).all()
    for user in users:
        st.write(f"{user.name} ({user.email}) - {user.role}")

    session.close()
