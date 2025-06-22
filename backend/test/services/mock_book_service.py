"""Mock implementation of the BookServiceBase class."""
from app.models.book_dto import BookResponse
from app.services.book_service_base import BookServiceBase
from app.utils.isbn_utils import is_valid_isbn10, is_valid_isbn13


class MockBookService(BookServiceBase):
    """Mock implementation of the BookServiceBase class."""

    def __init__(self):
        """Initialize store to simulate access to Redis instance or ISBNdb API."""
        self._store = {}

    def fetch_book(self, book_shelf=None, isbn10=None, isbn13=None):
        """Fetch a book by ISBN-10 or ISBN-13 from the mock store."""
        self._validate_isbn(isbn10, isbn13)
        key = isbn13 or isbn10
        if not key:
            raise ValueError("At least one of ISBN-10 or ISBN-13 must be provided.")

        return self._store.get(key).to_dict()

    def search_books(self, query: str, page: int, limit: int) -> dict:
        """
        Mock search functionality.

        Returns books whose title contains the query string (case insensitive).
        """
        matching_books = [
            book.to_dict() for book in self._store.values()
            if query.lower() in book.title.lower()
        ]

        # Simulate pagination
        start = (int(page) - 1) * int(limit)
        end = start + int(limit)
        paginated_books = matching_books[start:end]

        return {
            "success": True,
            "books": paginated_books,
            "page": int(page),
            "limit": int(limit),
            "total_results": len(matching_books),
        }

    @staticmethod
    def _validate_isbn(isbn10, isbn13):
        """Validate the provided ISBNs to ensure they are in a correct format."""
        if not is_valid_isbn10(isbn10) and not is_valid_isbn13(isbn13):
            print(f'isbn13: {isbn13}')
            raise ValueError("Both ISBN-10 and ISBN-13 are invalid.")

    def mock_books(self, books: list[BookResponse]):
        """Mock multiple books in the store for testing."""
        for book in books:
            key = book.isbn13 or book.isbn10
            if not key:
                raise ValueError("Book must have either an ISBN-10 or ISBN-13.")
            self._store[key] = book
