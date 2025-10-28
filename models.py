from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime, timezone
import bcrypt

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    name = Column(String(100), nullable=False)
    role = Column(String(20), default='user')  # user or admin
    address = Column(Text)
    phone = Column(String(20))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    rentals = relationship("Rental", back_populates="user")
    reviews = relationship("Review", back_populates="user")
    wishlist = relationship("Wishlist", back_populates="user")

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    author = Column(String(100), nullable=False)
    genre = Column(String(50))
    description = Column(Text)
    price_per_day = Column(Float, nullable=False)
    stock = Column(Integer, default=1)
    available = Column(Integer, default=1)
    cover_image = Column(String(255))
    isbn = Column(String(20))
    published_year = Column(Integer)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    rentals = relationship("Rental", back_populates="book")
    reviews = relationship("Review", back_populates="book")
    wishlists = relationship("Wishlist", back_populates="book")

class Rental(Base):
    __tablename__ = 'rentals'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    book_id = Column(Integer, ForeignKey('books.id'))
    rent_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    due_date = Column(DateTime, nullable=False)
    return_date = Column(DateTime)
    status = Column(String(20), default='active')  # active, returned, overdue
    total_amount = Column(Float, nullable=False)
    late_fee = Column(Float, default=0.0)
    user = relationship("User", back_populates="rentals")
    book = relationship("Book", back_populates="rentals")
    payment = relationship("Payment", back_populates="rental", uselist=False)

class Payment(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True)
    rental_id = Column(Integer, ForeignKey('rentals.id'))
    amount = Column(Float, nullable=False)
    status = Column(String(20), default='pending')  # pending, completed, failed
    payment_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    rental = relationship("Rental", back_populates="payment")

class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    book_id = Column(Integer, ForeignKey('books.id'))
    rating = Column(Integer, nullable=False)  # 1-5
    comment = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    user = relationship("User", back_populates="reviews")
    book = relationship("Book", back_populates="reviews")

class Wishlist(Base):
    __tablename__ = 'wishlists'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    book_id = Column(Integer, ForeignKey('books.id'))
    added_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    user = relationship("User", back_populates="wishlist")
    book = relationship("Book", back_populates="wishlists")

# Database setup
engine = create_engine('sqlite:///book_rental.db', echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
