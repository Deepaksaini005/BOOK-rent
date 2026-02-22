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
    if "add_book" in st.session_state and st.session_state.add_book:
        with st.form("add_book_form"):
            title = st.text_input("Title *", placeholder="Book title")
            author = st.text_input("Author *", placeholder="Author name")
            genre = st.text_input("Genre", placeholder="e.g. Novel, Fiction")
            price = st.number_input("Price per day ($)", min_value=0.0, value=3.0, step=0.5)
            stock = st.number_input("Stock", min_value=1, value=1)
            description = st.text_area("Description", placeholder="Short description")
            if st.form_submit_button("Add Book"):
                t = (title or "").strip()
                a = (author or "").strip()
                if not t or not a:
                    st.error("Title and Author are required.")
                else:
                    try:
                        book = Book(
                            title=t,
                            author=a,
                            genre=(genre or "").strip() or None,
                            price_per_day=price,
                            stock=stock,
                            available=stock,
                            description=(description or "").strip() or None,
                        )
                        session.add(book)
                        session.commit()
                        st.success("Book added!")
                        st.session_state.add_book = False
                        st.rerun()
                    except Exception as e:
                        session.rollback()
                        st.error(f"Could not add book: {str(e)}")

    # Edit book form
    if "edit_book" in st.session_state:
        book = st.session_state.edit_book
        # Re-attach to current session for update
        db_book = session.query(Book).filter_by(id=book.id).first()
        if not db_book:
            del st.session_state.edit_book
            st.rerun()
        else:
            st.subheader(f"Edit Book: {db_book.title}")
            with st.form("edit_book_form"):
                title = st.text_input("Title", db_book.title)
                author = st.text_input("Author", db_book.author)
                genre = st.text_input("Genre", db_book.genre or "")
                price = st.number_input("Price per day", min_value=0.0, value=float(db_book.price_per_day))
                stock = st.number_input("Stock", min_value=1, value=db_book.stock)
                description = st.text_area("Description", db_book.description or "")
                if st.form_submit_button("Update Book"):
                    db_book.title = title
                    db_book.author = author
                    db_book.genre = genre
                    db_book.price_per_day = price
                    db_book.stock = stock
                    db_book.available = min(db_book.available, stock)
                    db_book.description = description
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
                try:
                    session.delete(book)
                    session.commit()
                    st.success("Book deleted!")
                    st.rerun()
                except Exception as e:
                    session.rollback()
                    st.error("Cannot delete: book has rentals, reviews, or wishlist entries. Remove them first.")

    # Manage Users
    st.subheader("👥 Manage Users")
    users = session.query(User).all()
    for user in users:
        st.write(f"{user.name} ({user.email}) - {user.role}")

    session.close()
