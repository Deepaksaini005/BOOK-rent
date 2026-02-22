from models import Session, User, Book, Rental, Review, Wishlist, Payment
from datetime import datetime, timedelta
import plotly.express as px
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

def get_session():
    return Session()

def init_db():
    from models import engine, Base
    Base.metadata.create_all(engine)
    session = get_session()
    try:
        admin = session.query(User).filter_by(email='admin@bookrent.com').first()
        if not admin:
            admin = User(email='admin@bookrent.com', name='Admin', role='admin')
            admin.set_password('admin123')
            session.add(admin)
            session.commit()

        if session.query(Book).count() == 0:
            sample_books = [
            # Novels
            Book(title="To Kill a Mockingbird", author="Harper Lee", genre="Novel", description="A gripping tale of racial injustice and childhood innocence.", price_per_day=3.50, stock=5, available=5, published_year=1960),
            Book(title="1984", author="George Orwell", genre="Novel", description="A dystopian social science fiction novel.", price_per_day=4.00, stock=4, available=4, published_year=1949),
            Book(title="Pride and Prejudice", author="Jane Austen", genre="Novel", description="A romantic novel of manners.", price_per_day=3.00, stock=6, available=6, published_year=1813),
            Book(title="The Great Gatsby", author="F. Scott Fitzgerald", genre="Novel", description="A classic American novel about the Jazz Age.", price_per_day=3.50, stock=5, available=5, published_year=1925),
            Book(title="One Hundred Years of Solitude", author="Gabriel García Márquez", genre="Novel", description="A multi-generational saga of the Buendía family.", price_per_day=4.50, stock=3, available=3, published_year=1967),

            # Biographies
            Book(title="Steve Jobs", author="Walter Isaacson", genre="Biography", description="The definitive biography of Steve Jobs.", price_per_day=5.00, stock=4, available=4, published_year=2011),
            Book(title="The Autobiography of Malcolm X", author="Malcolm X", genre="Biography", description="The life story of Malcolm X.", price_per_day=4.00, stock=5, available=5, published_year=1965),
            Book(title="Educated", author="Tara Westover", genre="Biography", description="A memoir about education and family.", price_per_day=4.50, stock=4, available=4, published_year=2018),
            Book(title="Becoming", author="Michelle Obama", genre="Biography", description="Michelle Obama's memoir.", price_per_day=5.50, stock=3, available=3, published_year=2018),

            # Science Fiction
            Book(title="Dune", author="Frank Herbert", genre="Science Fiction", description="A science fiction epic.", price_per_day=4.50, stock=4, available=4, published_year=1965),
            Book(title="Neuromancer", author="William Gibson", genre="Science Fiction", description="A cyberpunk novel.", price_per_day=4.00, stock=5, available=5, published_year=1984),

            # Mystery
            Book(title="The Girl with the Dragon Tattoo", author="Stieg Larsson", genre="Mystery", description="A psychological thriller.", price_per_day=4.50, stock=4, available=4, published_year=2005),
            Book(title="Gone Girl", author="Gillian Flynn", genre="Mystery", description="A thriller about a missing woman.", price_per_day=4.00, stock=5, available=5, published_year=2012),

            # History
            Book(title="Sapiens: A Brief History of Humankind", author="Yuval Noah Harari", genre="History", description="A book about the history of humanity.", price_per_day=5.00, stock=4, available=4, published_year=2011),
            Book(title="The Guns of August", author="Barbara Tuchman", genre="History", description="About the first month of World War I.", price_per_day=4.50, stock=3, available=3, published_year=1962),

            # Self-Help
            Book(title="Atomic Habits", author="James Clear", genre="Self-Help", description="A guide to building good habits.", price_per_day=4.00, stock=6, available=6, published_year=2018),
            Book(title="The Power of Habit", author="Charles Duhigg", genre="Self-Help", description="How habits work and how to change them.", price_per_day=4.50, stock=5, available=5, published_year=2012),

            # Fantasy
            Book(title="The Name of the Wind", author="Patrick Rothfuss", genre="Fantasy", description="A fantasy novel about a gifted young man.", price_per_day=4.50, stock=4, available=4, published_year=2007),
            Book(title="The Hobbit", author="J.R.R. Tolkien", genre="Fantasy", description="A fantasy adventure.", price_per_day=3.50, stock=6, available=6, published_year=1937),

            # Poetry
            Book(title="The Waste Land", author="T.S. Eliot", genre="Poetry", description="A modernist poem.", price_per_day=3.00, stock=4, available=4, published_year=1922),
            Book(title="Leaves of Grass", author="Walt Whitman", genre="Poetry", description="A collection of poetry.", price_per_day=3.50, stock=5, available=5, published_year=1855),
            ]
            for book in sample_books:
                session.add(book)
            session.commit()
    finally:
        session.close()

def calculate_rent_amount(book, days):
    return book.price_per_day * days

def calculate_late_fee(rental):
    if rental.return_date and rental.return_date > rental.due_date:
        days_late = (rental.return_date - rental.due_date).days
        return days_late * 5.0  # $5 per day late fee
    return 0.0

def generate_invoice(rental):
    """Generate invoice PDF and return filename (for backward compatibility)."""
    filename = f"invoice_{rental.id}.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    _draw_invoice_content(c, rental)
    c.save()
    return filename

def _draw_invoice_content(c, rental):
    c.drawString(100, 750, f"Invoice for Rental ID: {rental.id}")
    c.drawString(100, 730, f"User: {rental.user.name}")
    c.drawString(100, 710, f"Book: {rental.book.title}")
    c.drawString(100, 690, f"Rent Date: {rental.rent_date.strftime('%Y-%m-%d')}")
    c.drawString(100, 670, f"Due Date: {rental.due_date.strftime('%Y-%m-%d')}")
    c.drawString(100, 650, f"Total Amount: ${rental.total_amount:.2f}")
    if rental.late_fee and rental.late_fee > 0:
        c.drawString(100, 630, f"Late Fee: ${rental.late_fee:.2f}")
    c.drawString(100, 590, "Thank you for using Book Rental App!")

def generate_invoice_bytes(rental):
    """Generate invoice PDF and return as bytes for download."""
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    _draw_invoice_content(c, rental)
    c.save()
    buffer.seek(0)
    return buffer.getvalue()

def get_recommendations(user_id, session):
    # Simple recommendation based on user's past rentals
    user_rentals = session.query(Rental).filter_by(user_id=user_id).all()
    user_genres = [rental.book.genre for rental in user_rentals if rental.book.genre]
    if not user_genres:
        return session.query(Book).limit(5).all()
    # Recommend books from same genres
    recommended = session.query(Book).filter(Book.genre.in_(user_genres)).limit(5).all()
    return recommended

def get_analytics():
    session = get_session()
    # Total users
    total_users = session.query(User).count()
    # Total books
    total_books = session.query(Book).count()
    # Active rentals
    active_rentals = session.query(Rental).filter_by(status='active').count()
    # Total revenue
    total_revenue = session.query(Payment).filter_by(status='completed').with_entities(Payment.amount).all()
    total_revenue = sum([p[0] for p in total_revenue])
    session.close()
    return {
        'total_users': total_users,
        'total_books': total_books,
        'active_rentals': active_rentals,
        'total_revenue': total_revenue
    }

def create_charts():
    session = get_session()
    try:
        rentals = session.query(Rental).join(Book).all()
        genre_counts = {}
        for rental in rentals:
            genre = rental.book.genre or "Unknown"
            genre_counts[genre] = genre_counts.get(genre, 0) + 1
        if not genre_counts:
            genre_counts = {"No rentals yet": 0}
        fig = px.bar(
            x=list(genre_counts.keys()),
            y=list(genre_counts.values()),
            title="Rentals by Genre",
            labels={"x": "Genre", "y": "Count"},
        )
        return fig
    finally:
        session.close()
