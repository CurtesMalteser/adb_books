"""
This module declares the shelf Blueprint and the respective routes for the application.

It provides endpoints to CRUD operations on books in a user's shelf, with authentication and CORS support.
"""
from flask import Blueprint, request
from flask_cors import cross_origin

from app.auth.auth import requires_auth
from app.shelf.book import (store_book,
                            get_book,
                            remove_book,
                            update_book_shelf,
                            )

shelf_bp = Blueprint('shelf', __name__)


@shelf_bp.route('/book', methods=['POST'])
@cross_origin()
@requires_auth('book:add_to_shelf')
def add_book(payload):
    """Adds a book to the user's shelf."""
    return store_book(payload=payload, request=request)


@shelf_bp.route('/book/<string:book_id>')
@cross_origin()
@requires_auth('book:get_details')
def fetch_book(payload, book_id: str):
    """Fetches a book from the user's shelf."""
    user_id = payload.get('sub')
    return get_book(user_id=user_id, book_id=book_id)


@shelf_bp.route('/book/<string:book_id>', methods=['DELETE'])
@cross_origin()
@requires_auth('book:delete_shelf')
def delete_book(payload, book_id: str):
    """Deletes a book from the user's shelf."""
    user_id = payload.get('sub')
    return remove_book(user_id=user_id, book_id=book_id)


@shelf_bp.route('/book/<string:book_id>', methods=['PATCH'])
@cross_origin()
@requires_auth('book:update_shelf')
def patch_book_shelf(payload, book_id: str):
    """Updates a book in the user's shelf."""
    user_id = payload.get('sub')
    return update_book_shelf(user_id=user_id, book_id=book_id, request=request)
