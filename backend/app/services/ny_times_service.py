"""
This module contains the concrete implementation of the NYTimesServiceBase interface.

The class fetches bestsellers list from a Redis instance or from the NYTimes API.
"""
import json
import os
from urllib.parse import urljoin

import redis
import requests
from flask import (
    abort,
)
from redis.typing import ResponseT
from requests import (
    JSONDecodeError,
    RequestException,
)

from app.config import (
    NY_TIMES_BOOKS_LIST_URL, REDIS_EXPIRY_TIME,
)
from app.models.book_dto import BookResponse
from app.services.ny_times_service_base import NYTimesServiceBase


class NyTimesService(NYTimesServiceBase):
    """Concrete implementation of the NYTimesServiceBase interface."""
    _api_key = os.environ.get('NYT_KEY')

    def __init__(self, redis_client: redis.Redis):
        """Initializes the NyTimesService with a Redis client."""
        self.redis_client = redis_client

    def fetch_books(self, path: str, page: int, limit: int) -> dict:
        """
        Fetches bestsellers list from a Redis instance or from the NYTimes API.

        :param path: fiction, non-fiction, etc.
        :param page: the page number.
        :param limit: booklist response maximum size.
        :return: JSON dictionary containing the bestsellers list.
        """
        try:

            bestsellers = self.redis_client.get(f'nyt_bestsellers_{path}')
            if bestsellers:
                json_books = self._redis_json(path=path, bestsellers=bestsellers)
                return {
                    'success': True,
                    'books': json_books,
                    'page': page,
                    'limit': limit,
                    'total_results': len(json_books)
                }

            else:
                response = requests.get(self._url(path))
                response.raise_for_status()
                json_response = response.json()
                total_results = json_response.get('num_results')
                json_books = self._bestsellers_json(json_response=json_response, path=path)
                return {
                    'success': True,
                    'books': json_books,
                    'page': page,
                    'limit': limit,
                    'total_results': total_results
                }

        except JSONDecodeError as e:
            print(e)
            abort(500, description="Invalid JSON response from upstream server.")

        except RequestException as e:
            print(e)
            abort(500, description=f"An error occurred while fetching data: {str(e)}")

    def _url(self, path: str):
        return urljoin(NY_TIMES_BOOKS_LIST_URL, f'{path}?api-key={self._api_key}')

    def _redis_json(self, path: str, bestsellers: ResponseT) -> list[dict]:
        """
        Converts the bestsellers JSON string from Redis into a list of dictionaries.

        :param path: NYT bestsellers list name; e.g. 'non-fiction'.
        :param bestsellers: ResponseT from Redis.
        :return: books as a list of dictionaries or raise.
        """
        try:
            json_books = json.loads(bestsellers)
            json_books = [BookResponse.from_json(d).to_dict() for d in json_books]
            return json_books
        except Exception as e:
            self.redis_client.delete(f'nyt_bestsellers_{path}')
            raise e

    def _bestsellers_json(self, path: str, json_response) -> list[dict]:
        """
        Converts the bestsellers JSON string from Redis into a list of dictionaries.

        :param path: NYT bestsellers list name; e.g. 'non-fiction'.
        :param json_response: ResponseT from Redis.
        :return: books as a list of dictionaries or raise.
        """
        try:
            json_books = json_response.get('results').get('books')
            json_books = [BookResponse.from_ny_times_json(d).to_dict() for d in json_books]
            self.redis_client.set(f'nyt_bestsellers_{path}', json.dumps(json_books), ex=REDIS_EXPIRY_TIME)
            return json_books
        except Exception as e:
            raise e
