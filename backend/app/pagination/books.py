from flask import (
    jsonify,
    abort,
)
from app.models.book import Book


def paginate(request, query):
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 10, type=int)
    size = size if size <= 10 else 10
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