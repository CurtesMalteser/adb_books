"""
This module contains the Search API for fetching book data from app databases or external APIs.

Used by the search blueprint.
"""
import os

import inject
from flask import (
    request,
    jsonify,
    abort,
)
from requests import (
    JSONDecodeError,
    RequestException,
    HTTPError,
)

from app.config import (
    DEFAULT_PAGE,
    DEFAULT_LIMIT,
)
from app.exceptions.invalid_request_error import InvalidRequestError
from app.services.book_service_base import BookServiceBase

api_key = os.environ.get('ISBNDB_KEY')


@inject.params(book_service=BookServiceBase)
def books(book_service: BookServiceBase):
    """
    Fetches book based on the search query provided in the request.

    :param book_service: BookServiceBase instance for fetching book data.
    :type book_service: BookServiceBase

    :return: JSON array of books if the request is successful, or aborts with an error response.
    :rtype: list or flask.Response
    """
    query = request.args.get('q')
    page = request.args.get('page', default=DEFAULT_PAGE)
    limit = request.args.get('limit', default=DEFAULT_LIMIT)

    if not query:
        raise InvalidRequestError(message="Missing 'q' parameter", code=400)

    try:
        result = book_service.search_books(query=query, page=page, limit=limit)
        return jsonify(result)

    except JSONDecodeError:
        abort(500, description="Invalid JSON response from upstream server.")

    except HTTPError as e:
        if e.response.status_code == 404:
            abort(404, description="Resource not found.")
        else:
            abort(500, description=f"An error occurred while fetching data: {str(e)}")

    except RequestException as e:
        abort(500, description=f"An error occurred while fetching data: {str(e)}")
