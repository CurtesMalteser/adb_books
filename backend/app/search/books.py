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
    SEARCH_ENDPOINT,
    DEFAULT_PAGE,
    DEFAULT_LIMIT,
)
from app.exceptions.invalid_request_error import InvalidRequestError
from app.models.book import Book

api_key = os.environ.get('ISBNDB_KEY')

def books(user_agent):
    """
    :param user_agent: The user agent string to be used in the request headers.
    :type user_agent: str

    :return: JSON array of books if the request is successful, or aborts with an error response.
    :rtype: list or flask.Response
    """
    query = request.args.get('q')
    page = request.args.get('page', default=DEFAULT_PAGE)
    limit = request.args.get('limit', default=DEFAULT_LIMIT)

    if not query:
        raise  InvalidRequestError(message="Missing 'q' parameter", code=400)

    url = urljoin(SEARCH_ENDPOINT,f'{query}?page={page}&pageSize={limit}')

    headers = {
        "User-Agent": user_agent,
        "Authorization": api_key
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        json = response.json()
        total_results = json.get('total')
        json_books = json.get('books')
        json_books = map(lambda d: Book.from_json(d=d), json_books)

        return jsonify(
            {
                'success': True,
                'books': list(json_books),
                'page': page,
                'limit': limit,
                'total_results': total_results
            }
        )  # Flask's jsonify adds the correct content type headers automatically

    except JSONDecodeError:
        abort(500, description="Invalid JSON response from upstream server.")

    except RequestException as e:
        abort(500, description=f"An error occurred while fetching data: {str(e)}")