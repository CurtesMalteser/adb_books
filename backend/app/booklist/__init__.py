from flask import Blueprint

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
@requires_auth('booklist:get')
def fetch_booklist(payload, shelf: str):
    user_id = payload.get('sub')
    print(f'👤 {user_id}')
    if _is_shelf(shelf):
        return booklist(used_id=user_id, shelf=shelf)
    else:
        raise InvalidRequestError(code=404, message=f'Shelf: \'{shelf}\' not found.')
