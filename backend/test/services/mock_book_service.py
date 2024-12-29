"""
Mock implementation of the BookServiceBase class.
"""
from app.models.book_dto import BookResponse
from app.services.book_service_base import BookServiceBase
from app.utils.isbn_utils import is_valid_isbn_10, is_valid_isbn_13


class MockBookService(BookServiceBase):
    """
    Mock implementation of the BookServiceBase class.
    """

    def __init__(self):
        # Initialize store to simulate access to Redis instance or ISBNdb API
        self._store = {}

    def fetch_book(self, book_shelf=None, isbn_10=None, isbn_13=None):
        """
        Fetch a book by ISBN-10 or ISBN-13 from the mock store.
        """
        self._validate_isbn(isbn_10, isbn_13)
        key = isbn_13 or isbn_10
        if not key:
            raise ValueError("At least one of ISBN-10 or ISBN-13 must be provided.")

        return self._store.get(key).to_dict()

    @staticmethod
    def _validate_isbn(isbn_10, isbn_13):
        """
        Validate the provided ISBNs to ensure they are in a correct format.
        """
        if isbn_10 and not is_valid_isbn_10(isbn_10):
            raise ValueError("Invalid ISBN-10 format.")

        if isbn_13 and not is_valid_isbn_13(isbn_13):
            raise ValueError("Invalid ISBN-13 format.")

    def mock_books(self, books: list[BookResponse]):
        """
        Mock multiple books in the store for testing.
        """
        for book in books:
            key = book.isbn13 or book.isbn10
            if not key:
                raise ValueError("Book must have either an ISBN-10 or ISBN-13.")
            self._store[key] = book
