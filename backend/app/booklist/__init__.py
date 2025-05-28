"""This module provides a Flask blueprint for handling booklist-related routes."""
from flask import Blueprint
from flask_cors import cross_origin

from app.auth.auth import requires_auth
from app.booklist.booklist import booklist
from app.exceptions.invalid_request_error import InvalidRequestError

booklist_bp = Blueprint('booklist', __name__)


def _is_shelf(value):
    match value:
        case 'read' | 'want-to-read' | 'currently-reading':
            return True
        case _:
            return False


@booklist_bp.route('/booklist/<string:shelf>')
@cross_origin()
@requires_auth('booklist:get')
def fetch_booklist(payload, shelf: str):
    """
    Fetches a booklist by shelf type.

    :param payload: The payload containing user information, typically including the user ID.
    :type payload: dict
    :param shelf: The type of shelf to fetch books from. Must be one of 'read', 'want-to-read', or 'currently-reading'.
    :type shelf: str
    :return: A JSON response containing a list of books stored in the specified shelf.
    :rtype: flask.Response
    """
    user_id = payload.get('sub')
    if _is_shelf(shelf):
        return booklist(used_id=user_id, shelf=shelf)
    else:
        raise InvalidRequestError(code=404, message=f'Shelf: \'{shelf}\' not found.')
