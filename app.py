import streamlit as st
from views import home, login, register, dashboard, admin_dashboard, book_details, search_books, rent_book, my_rentals, wishlist, reviews, profile
from utils import init_db, get_session
from models import User

# Initialize database
init_db()

# Page configuration
st.set_page_config(page_title="Book Rental App", page_icon="📚", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header { font-size: 2rem; font-weight: 700; color: #1e3a5f; margin-bottom: 0.5rem; }
    .sub-header { color: #5a7a9a; margin-bottom: 1.5rem; }
    .stMetric { background: linear-gradient(135deg, #f0f7ff 0%, #e8f4fc 100%); padding: 1rem; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
    div[data-testid="stSidebar"] { background: linear-gradient(180deg, #f8fbfd 0%, #eef5fc 100%); }
    .book-card { background: #fff; border-radius: 12px; padding: 1.25rem; box-shadow: 0 2px 12px rgba(0,0,0,0.08); margin-bottom: 1rem; border: 1px solid #e8eef5; }
    .stButton > button { border-radius: 8px; font-weight: 500; transition: all 0.2s; }
    .stButton > button:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(0,0,0,0.12); }
    section.main .block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 1200px; }
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
def sidebar():
    st.sidebar.title("📚 Book Rental App")
    if 'user' not in st.session_state:
        st.session_state.user = None

    if st.session_state.user:
        st.sidebar.write(f"Welcome, **{st.session_state.user.name}**!")
        if st.sidebar.button("Logout"):
            st.session_state.user = None
            if 'selected_book' in st.session_state:
                del st.session_state.selected_book
            st.rerun()
        st.sidebar.markdown("---")
        st.sidebar.subheader("Navigation")
        nav_options = ["Home", "Dashboard", "Search Books", "My Rentals", "Wishlist", "My Reviews", "Profile"]
        if st.session_state.get("selected_book"):
            nav_options.insert(3, "Book Details")
            nav_options.insert(4, "Rent Book")
        if st.session_state.user.role == "admin":
            nav_options.append("Admin Dashboard")
        page = st.sidebar.radio("Go to", nav_options, key="nav_radio")
    else:
        page = st.sidebar.radio("Go to", ["Home", "Login", "Register"], key="nav_radio")

    return page

# Main app
def main():
    page = sidebar()

    if page == "Home":
        home.show()
    elif page == "Dashboard":
        dashboard.show()
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
    elif page == "My Reviews":
        reviews.show()
    elif page == "Profile":
        profile.show()
    else:
        st.error("Page not found")

if __name__ == "__main__":
    main()
