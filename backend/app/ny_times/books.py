import inject
from flask import (
    request,
    jsonify,
)

from app.config import (
    DEFAULT_PAGE,
    DEFAULT_LIMIT,
)
from app.services.ny_times_service_base import NYTimesServiceBase


@inject.params(book_service=NYTimesServiceBase)
def fetch_books(path: str, book_service: NYTimesServiceBase):
    """
    Fetches bestseller data provided by The New York Times.
    Visit https://api.nytimes.com/svc/books/v3/lists/names.json?api-key=<api_key> for available list names.
    :param path: The list_name_encoded field from the provided URL.
    :param book_service: NYTimesServiceBase instance.
    :return: JSON array of books if the request is successful, or aborts with an error response.
    :rtype: list or flask.Response
    """
    page = request.args.get('page', default=DEFAULT_PAGE)
    limit = request.args.get('limit', default=DEFAULT_LIMIT)

    response_dict = book_service.fetch_books(path, page, limit)
    return jsonify(response_dict)
