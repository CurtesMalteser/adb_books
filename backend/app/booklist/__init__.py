from flask import Blueprint

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
def fetch_booklist(shelf: str):
    if _is_shelf(shelf):
        return booklist(shelf)
    else:
        raise InvalidRequestError(code=404, message=f'Shelf: \'{shelf}\' not found.')
