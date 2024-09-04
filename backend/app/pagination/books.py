from flask import (
    jsonify,
    abort,
)

from app.config import DEFAULT_PAGE, DEFAULT_LIMIT
from app.models.book import Book


def paginate(request, query):
    """
    Parses the query parameters from the received request and fetches book results from the database.

    :param request: The incoming HTTP request that may contain query parameters.
    :type request: flask.Request
    :param query: The query object used to fetch results from the database.
    :type query: BookDto

    :return: A JSON response containing the success status, book data, pagination details, and total results.
    :rtype: flask.Response or None
    """

    page = request.args.get('page', DEFAULT_PAGE, type=int)
    size = request.args.get('limit', DEFAULT_LIMIT, type=int)
    size = size if size <= DEFAULT_LIMIT else DEFAULT_LIMIT
    start = (page - 1) * size
    end = start + size

    data_books = []

    try:
        data_books = query()
    except:
        abort(500)

    total_results = len(data_books)
    data_books = map(lambda book: Book(
        id=book.bookId,
        title=book.title,
        author=book.author,
        rating=book.rating
    ), data_books
                     )

    data_books = list(data_books)[start:end]

    if len(data_books) > 0:
        return jsonify({
            'success': True,
            'books': data_books,
            'page': page,
            'page_size': size,
            'total_results': total_results
        })
    else:
        return None