from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from books.models import Book, Author
from reviews.models import Review
from django.utils.timezone import now

class BookAPITestCase(TestCase):
    def setUp(self):
        """Set up test data before each test"""
        self.client = APIClient()
        
        # Create test user and authenticate
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)

        # Create authors
        self.author1 = Author.objects.create(name="J.K. Rowling", biography="Famous author", date_of_birth="1965-07-31", nationality="British")
        self.author2 = Author.objects.create(name="George R.R. Martin", biography="Fantasy writer", date_of_birth="1948-09-20", nationality="American")

        # Create a book
        self.book = Book.objects.create(
            title="Harry Potter and the Chamber of Secrets",
            isbn="9780747538493",
            publication_date="1998-07-02",
            price="29.99",
            stock=50,
            genre="Fantasy",
            description="Second book in Harry Potter series.",
            publisher="Bloomsbury"
        )
        self.book.authors.add(self.author1)

        # Create a review
        self.review = Review.objects.create(
            user=self.user,
            book=self.book,
            rating=5,
            comment="Amazing book!",
            created_at=now()
        )

    def test_get_books_list(self):
        """Test retrieving all books with authentication"""
        response = self.client.get("/book/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)  # Ensure books exist

    def test_get_book_detail(self):
        """Test retrieving a single book with authors and reviews"""
        response = self.client.get(f"/book/books/{self.book.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.book.title)
        self.assertIn("authors", response.data)
        self.assertIn("reviews", response.data)

    def test_create_book(self):
        """Test creating a new book"""
        book_data = {
            "title": "A Game of Thrones",
            "isbn": "9780553103540",
            "publication_date": "1996-08-06",
            "price": "49.99",
            "stock": 30,
            "genre": "Fantasy",
            "description": "First book in the A Song of Ice and Fire series.",
            "publisher": "Bantam Books",
            "author_ids": [self.author2.id]  
        }
        response = self.client.post("/book/books/", book_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "A Game of Thrones")

    def test_delete_book_soft(self):
        """Test soft deleting a book"""
        response = self.client.delete(f"/book/books/{self.book.id}/delete/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.book.refresh_from_db()
        self.assertTrue(self.book.is_deleted)


    def test_get_books_with_filter(self):
        """Test filtering books by author"""
        response = self.client.get(f"/book/books/?authors={self.author1.id}")
        print(response.data['results'][0]["title"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Ensure that books are actually returned
        self.assertGreater(len(response.data), 0, "No books returned for the given author filter.")
        
        self.assertEqual(response.data['results'][0]["title"], self.book.title)


    def test_review_creation(self):
        """Test posting a new review for a book"""
        review_data = {
            "user": self.user.id,
            "book": self.book.id,
            "rating": 4,
            "comment": "Great book, but a bit long!",
        }
        response = self.client.post("/review/", review_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["rating"], 4)
        self.assertEqual(response.data["comment"], "Great book, but a bit long!")

    def test_unauthenticated_access(self):
        """Test that unauthenticated users cannot access certain endpoints"""
        self.client.force_authenticate(user=None)  # Logout user
        response = self.client.get("/book/books/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
