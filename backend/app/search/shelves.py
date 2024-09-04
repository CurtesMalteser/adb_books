from flask import (
    request,
    jsonify,
    abort,
)
from app.exceptions.invalid_request_error import InvalidRequestError
from app.models.book_dto import BookDto
from app.pagination.books import paginate


def shelves():
    query_param = request.args.get('q')

    if not query_param:
        print("No query")
        raise InvalidRequestError(message="Missing 'q' parameter", code=400)

    try:
        query = lambda : BookDto.query.filter(BookDto.title.ilike('%{}%'.format(query_param))).order_by(BookDto.id).all()
        books = paginate(request=request, query=query)

        if books is None:
            return jsonify({
                'success': True,
                'books': [],
                'page': 0,
                'page_size': 0,
                'total_results': 0
                })
        else:
            return books

    except Exception as e:
        print(e)
        abort(400)