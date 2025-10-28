import streamlit as st
from views import home, login, register, dashboard, admin_dashboard, book_details, search_books, rent_book, my_rentals, wishlist, reviews, profile
from utils import init_db, get_session
from models import User

# Initialize database
init_db()

# Page configuration
st.set_page_config(page_title="Book Rental App", page_icon="📚", layout="wide")

# Sidebar navigation
def sidebar():
    st.sidebar.title("📚 Book Rental App")
    if 'user' not in st.session_state:
        st.session_state.user = None

    if st.session_state.user:
        st.sidebar.write(f"Welcome, {st.session_state.user.name}!")
        if st.sidebar.button("Logout"):
            st.session_state.user = None
            st.rerun()
        st.sidebar.markdown("---")
        st.sidebar.subheader("Navigation")
        page = st.sidebar.radio("Go to", ["Home", "Search Books", "My Rentals", "Wishlist", "Profile"])
        if st.session_state.user.role == 'admin':
            page = st.sidebar.radio("Go to", ["Home", "Search Books", "My Rentals", "Wishlist", "Profile", "Admin Dashboard"])
    else:
        page = st.sidebar.radio("Go to", ["Home", "Login", "Register"])

    return page

# Main app
def main():
    page = sidebar()

    if page == "Home":
        home.show()
    elif page == "Login":
        login.show()
    elif page == "Register":
        register.show()
    elif page == "Admin Dashboard":
        admin_dashboard.show()
    elif page == "Search Books":
        search_books.show()
    elif page == "Book Details":
        book_details.show()
    elif page == "Rent Book":
        rent_book.show()
    elif page == "My Rentals":
        my_rentals.show()
    elif page == "Wishlist":
        wishlist.show()
    elif page == "Reviews":
        reviews.show()
    elif page == "Profile":
        profile.show()
    else:
        st.error("Page not found")

if __name__ == "__main__":
    main()
