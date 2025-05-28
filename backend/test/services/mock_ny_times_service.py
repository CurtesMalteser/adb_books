"""
This module contains the concrete implementation of the NYTimesServiceBase interface.

The class fetches bestsellers list from a Redis instance or from the NYTimes API.
"""
import os

from app.services.ny_times_service_base import NYTimesServiceBase


class MockNyTimesService(NYTimesServiceBase):
    """Mock implementation of the NYTimesServiceBase interface."""
    _api_key = os.environ.get('NYT_KEY')

    def __init__(self):
        """Initialize the MockNyTimesService class."""
        # Initialize store to simulate access to Redis instance or NYT API
        self._store = {}
        self._mock_error = False

    def fetch_books(self, path: str, page: int, limit: int) -> dict:
        """
        Fetches bestsellers list from sef._store. Call mock_books to populate the store.

        :param path: fiction, non-fiction, etc.
        :param page: the page number.
        :param limit: booklist response maximum size.
        :return: JSON dictionary containing the bestsellers list.
        """
        if self._mock_error:
            raise ValueError("Internal Server Error")

        if path not in self._store:
            raise ValueError(f"Path '{path}' not found in store. Call mock_books to populate the store.")
        else:
            json_books = self._store[path]
            return {
                'success': True,
                'books': json_books,
                'page': page,
                'limit': limit,
                'total_results': len(json_books)
            }

    def mock_books(self, path: str, books: list[dict]):
        """Mocks the bestsellers list from the NYTimes API."""
        self._store[path] = books if path not in self._store else self._store[path] + books

    def mock_error(self, error: bool):
        """Mocks an error response."""
        self._mock_error = error
