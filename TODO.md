# Book Rental App Development Plan

## Phase 1: Project Setup
- [x] Create project structure (models/, views/, utils/, static/)
- [x] Create requirements.txt with dependencies
- [x] Set up database configuration

## Phase 2: Database Models
- [x] Create User model (id, email, password, name, role, etc.)
- [x] Create Book model (id, title, author, genre, price, stock, etc.)
- [x] Create Rental model (id, user_id, book_id, rent_date, due_date, status)
- [x] Create Review model (id, user_id, book_id, rating, comment)
- [x] Create Payment model (id, rental_id, amount, status)

## Phase 3: Authentication
- [x] Implement user registration
- [x] Implement login/logout
- [x] Password hashing with bcrypt
- [x] Session management

## Phase 4: User Features
- [x] User dashboard
- [x] Book search and filtering
- [x] Book details page
- [x] Renting system (select duration, calculate price)
- [x] Wishlist management
- [x] Reviews and ratings
- [x] Rental history
- [x] Notifications (mock email)

## Phase 5: Admin Features
- [x] Admin login
- [x] Book management (add/edit/delete)
- [x] User management
- [x] Rental management
- [x] Analytics dashboard with charts

## Phase 6: Advanced Features
- [ ] AI recommendations (basic similarity)
- [ ] Smart search with auto-suggest
- [ ] Dynamic pricing
- [ ] Late fee calculator
- [ ] PDF invoice generation

## Phase 7: UI/UX
- [ ] Modern homepage with sections
- [ ] Responsive design
- [ ] Dark/light mode toggle
- [ ] Animations and transitions

## Phase 8: Testing and Deployment
- [ ] Test all features
- [ ] Deploy to Streamlit Cloud
- [ ] Add error handling and security

## Bug Fixes and Improvements
- [ ] Fix navigation issues: Add missing pages to sidebar (Book Details, Rent Book, Dashboard)
- [ ] Fix wishlist add functionality in search_books.py
- [ ] Fix book edit in admin_dashboard.py
- [ ] Add missing datetime import in dashboard.py
- [ ] Update rental return to calculate late_fee
- [ ] Improve invoice download in my_rentals.py
- [ ] Optimize genre filter query in search_books.py
- [ ] Add book delete in admin_dashboard.py
- [ ] Integrate payment in book_details.py or fix navigation
- [ ] Add error handling for database operations
- [ ] Add validation for forms
- [ ] Test all functionalities
