import os
from urllib.parse import urljoin

from flask import (
    request,
    jsonify,
    abort,
)
import requests
from requests import (
    JSONDecodeError,
    RequestException,
)

from app.config import (
    DEFAULT_PAGE,
    DEFAULT_LIMIT,
    NY_TIMES_BOOKS_LIST_URL,
)
from app.models.book_dto import BookResponse

api_key = os.environ.get('NYT_KEY')


def _url(path: str):
    return urljoin(NY_TIMES_BOOKS_LIST_URL, f'{path}?api-key={api_key}')


def fetch_books(path: str):
    """
    Fetches bestseller data provided by The New York Times.
    Visit https://api.nytimes.com/svc/books/v3/lists/names.json?api-key=<api_key> for available list names.
    :param path: The list_name_encoded field from the provided URL.
    :return: JSON array of books if the request is successful, or aborts with an error response.
    :rtype: list or flask.Response
    """

    page = request.args.get('page', default=DEFAULT_PAGE)
    limit = request.args.get('limit', default=DEFAULT_LIMIT)

    try:
        response = requests.get(_url(path))
        response.raise_for_status()
        json = response.json()
        total_results = json.get('num_results')
        json_books = json.get('results').get('books')
        json_books = map(lambda d: BookResponse.from_ny_times_json(d), json_books)

        return jsonify(
            {
                'success': True,
                'books': list(json_books),
                'page': page,
                'limit': limit,
                'total_results': total_results
            }
        )  # Flask's jsonify adds the correct content type headers automatically

    except JSONDecodeError as e:
        print(e)
        abort(500, description="Invalid JSON response from upstream server.")

    except RequestException as e:
        print(e)
        abort(500, description=f"An error occurred while fetching data: {str(e)}")
