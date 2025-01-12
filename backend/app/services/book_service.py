"""
This module defines the BookService class which is a concrete implementation of the BookServiceInterface.
The class fetches cached details from a Redis instance or from the ISBNdb API.
"""
import json
import os
from urllib.parse import urljoin

import redis
import requests

from app.config import GET_BOOK_ENDPOINT, REDIS_EXPIRY_TIME
from app.models.book import Book
from app.models.book_shelf import BookShelf
from app.services.book_service_base import BookServiceBase
from app.utils.isbn_utils import is_valid_isbn10, is_valid_isbn13


class BookService(BookServiceBase):
    """
    Concrete implementation of the BookServiceInterface.
    """
    _api_key = os.environ.get('ISBNDB_KEY')
    _user_agent = os.environ.get('USER_AGENT')

    headers = {
        "User-Agent": _user_agent,
        "Authorization": _api_key
    }

    def __init__(self, redis_client: redis.Redis):
        self.redis_client = redis_client

    def fetch_book(self, book_shelf: 'BookShelf', isbn10: str = None, isbn13: str = None) -> dict:
        """
        Fetches book details from the book service.
        """

        book_id = self._get_book_id(isbn10, isbn13)

        url = urljoin(GET_BOOK_ENDPOINT, book_id)

        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        json_response = response.json().get('book')

        book = Book.from_json(d=json_response)
        book_dict = book.to_dict()

        self.redis_client.set(book_id, json.dumps(book_dict), ex=REDIS_EXPIRY_TIME)

        book_dict['shelf'] = self.get_shelf_or_none(book_shelf)

        return book_dict

    @staticmethod
    def _get_book_id(isbn10: str = None, isbn13: str = None):
        """
        Returns the book ID based on the ISBN provided.
        """
        if isbn10 and not is_valid_isbn10(isbn10):
            raise ValueError("Invalid ISBN-10 format.")

        if isbn13 and not is_valid_isbn13(isbn13):
            raise ValueError("Invalid ISBN-13 format.")

        return isbn13 if isbn13 else isbn10
