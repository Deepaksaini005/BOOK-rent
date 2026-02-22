import unittest
from utils import calculate_rent_amount, calculate_late_fee, get_recommendations
from models import Base, User, Book, Rental
from datetime import datetime, timedelta, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class TestBookRentalApp(unittest.TestCase):
    def setUp(self):
        # Create in-memory database for testing
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        # Create test data
        self.user = User(name="Test User", email="test@example.com")
        self.user.set_password("password")
        self.session.add(self.user)

        self.book = Book(title="Test Book", author="Test Author", price_per_day=5.0, stock=10, available=10)
        self.session.add(self.book)
        self.session.commit()

    def tearDown(self):
        self.session.close()

    def test_calculate_rent_amount(self):
        amount = calculate_rent_amount(self.book, 7)
        self.assertEqual(amount, 35.0)

    def test_calculate_late_fee_no_late(self):
        now = datetime.now(timezone.utc)
        rental = Rental(
            user_id=self.user.id,
            book_id=self.book.id,
            rent_date=now - timedelta(days=5),
            due_date=now + timedelta(days=2),
            return_date=now,
            total_amount=25.0,
        )
        fee = calculate_late_fee(rental)
        self.assertEqual(fee, 0.0)

    def test_calculate_late_fee_with_late(self):
        now = datetime.now(timezone.utc)
        rental = Rental(
            user_id=self.user.id,
            book_id=self.book.id,
            rent_date=now - timedelta(days=10),
            due_date=now - timedelta(days=2),
            return_date=now,
            total_amount=50.0,
        )
        fee = calculate_late_fee(rental)
        self.assertEqual(fee, 10.0)  # 2 days late * $5/day

    def test_user_password_hashing(self):
        self.assertTrue(self.user.check_password("password"))
        self.assertFalse(self.user.check_password("wrongpassword"))

    def test_get_recommendations(self):
        now = datetime.now(timezone.utc)
        rental = Rental(
            user_id=self.user.id,
            book_id=self.book.id,
            rent_date=now,
            due_date=now + timedelta(days=7),
            total_amount=35.0,
        )
        self.session.add(rental)
        self.session.commit()

        recommendations = get_recommendations(self.user.id, self.session)
        self.assertIsInstance(recommendations, list)

if __name__ == '__main__':
    unittest.main()
