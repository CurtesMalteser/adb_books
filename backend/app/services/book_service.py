"""
This module defines the BookService class which is a concrete implementation of the BookServiceInterface.

The class fetches cached details from a Redis instance or from the ISBNdb API.
"""
import json
import os
from urllib.parse import urljoin

import redis
import requests

from app.config import GET_BOOK_ENDPOINT, REDIS_EXPIRY_TIME, SEARCH_ENDPOINT
from app.models.book import Book
from app.models.book_shelf import BookShelf
from app.services.book_service_base import BookServiceBase
from app.utils.isbn_utils import is_valid_isbn10, is_valid_isbn13


class BookService(BookServiceBase):
    """Concrete implementation of the BookServiceInterface."""
    _api_key = os.environ.get('ISBNDB_KEY')
    _user_agent = os.environ.get('USER_AGENT')

    headers = {
        "User-Agent": _user_agent,
        "Authorization": _api_key
    }

    def __init__(self, redis_client: redis.Redis):
        """
        Initializes the BookService with a Redis client.

        :param redis_client: Redis client instance for caching book data.
        """
        self.redis_client = redis_client

    def fetch_book(self, book_shelf: 'BookShelf', isbn10: str = None, isbn13: str = None) -> dict:
        """Fetches book details from the book service."""
        book_id = self._get_book_id(isbn10= isbn10, isbn13=isbn13)

        book = self.redis_client.get(book_id)

        if book is None:
            book_dict = self._fetch_book(book_id)
        else:
            book_dict = self._load_cached_book(book)

        # Add shelf information to the book details
        book_dict['shelf'] = self.get_shelf_or_none(book_shelf)

        return book_dict

    def _fetch_book(self, book_id):
        """
        Fetches book details from the ISBNdb API.

        :param book_id:
        :return: book details as a dictionary.
        """
        url = urljoin(GET_BOOK_ENDPOINT, book_id)
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        json_response = response.json().get('book')
        book = Book.from_json(d=json_response)
        book_dict = book.to_dict()
        self.redis_client.set(book_id, json.dumps(book_dict), ex=REDIS_EXPIRY_TIME)
        return book_dict

    def search_books(self, query: str, page: int, limit: int) -> dict:
        """
        Searches for books using the ISBNdb API based on the provided query.

        :param query: The search query string.
        :param page: The page number for paginated results.
        :param limit: The number of results per page.
        :return: A dictionary containing the search results, including success status, books, page, limit, and total results.
        """
        url = urljoin(SEARCH_ENDPOINT, f'{query}?page={page}&pageSize={limit}')
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        json_data = response.json()
        total_results = json_data.get('total')
        json_books = json_data.get('books')
        json_books = [Book.from_json(d).to_dict() for d in json_books]

        return {
            "success": True,
            "books": json_books,
            "page": page,
            "limit": limit,
            "total_results": total_results
        }

    @staticmethod
    def _load_cached_book(book):
        """
        Loads a cached book from Redis.

        :param book:
        :return: book details as a dictionary.
        """
        book = json.loads(book)
        book = Book.from_json(d=book)
        book_dict = book.to_dict()
        return book_dict

    @staticmethod
    def _get_book_id(isbn10: str = None, isbn13: str = None):
        """Returns the book ID based on the ISBN provided."""
        if isbn10 and not is_valid_isbn10(isbn10):
            raise ValueError("Invalid ISBN-10 format.")

        if isbn13 and not is_valid_isbn13(isbn13):
            raise ValueError("Invalid ISBN-13 format.")

        return isbn13 if isbn13 else isbn10
