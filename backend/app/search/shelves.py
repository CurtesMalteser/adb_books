"""
This module contains the Search API for fetching shelf data from app databases.

Used by the search blueprint.
"""
from flask import (
    request,
    abort,
)

from app.exceptions.invalid_request_error import InvalidRequestError
from app.models.book_dto import BookDto
from app.pagination.books import paginate


def shelves():
    """Searches for books by title based on the query parameter 'q'."""
    query_param = request.args.get('q')

    if not query_param:
        print("No query")
        raise InvalidRequestError(message="Missing 'q' parameter", code=400)

    try:
        return paginate(request=request, query=lambda: BookDto.search_by_title(query_param))

    except Exception as e:
        print(e)
        abort(400)
