from flask import Blueprint, request, jsonify, abort
from flask_cors import cross_origin

from app.auth.auth import requires_auth
from app.shelf.book import store_book, get_book, remove_book

shelf_bp = Blueprint('shelf', __name__)


@shelf_bp.route('/book', methods=['POST'])
@cross_origin()
@requires_auth('book:save')
def add_book(payload):
    print(f'👤 {payload}')
    return store_book(request)


@shelf_bp.route('/book/<string:book_id>')
@cross_origin()
def fetch_book(book_id: str):
    return get_book(book_id)


@shelf_bp.route('/book/<string:book_id>', methods=['DELETE'])
@cross_origin()
def delete_book(book_id: str):
    return remove_book(book_id)


# @TODO: add logic to update the shelf, rating might be something for the future
# @shelf_bp.route('/book/<string:book_id>', methods=['PATCH'])
# @cross_origin()
# def update_book_rating(book_id: str):
#     if request.is_json:
#         body = request.get_json()
#         try:
#             book = BookDto.query.filter(BookDto.id == book_id).one_or_none()
#
#             if book is None:
#                 abort(404)
#
#             if 'rating' in body:
#                 book.rating = int(body.get("rating"))
#
#             book.update()
#
#             return jsonify({
#                 "sucess": True,
#                 "updated": book_id,
#             })
#
#         except:
#             abort(400)