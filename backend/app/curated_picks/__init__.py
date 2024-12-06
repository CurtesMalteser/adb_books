from flask import Blueprint
from flask_cors import cross_origin

from app.auth.auth import requires_auth

curated_picks_bp = Blueprint('curated_picks', __name__)

# todo: define route for setting curated list
@curated_picks_bp.route('/curated-list', methods=['POST'])
@cross_origin()
@requires_auth('booklist:curator')
def add_curated_list(_):
    """
    Adds a curated list.
    :return: JSON object of the added curated list if the request is successful, or aborts with an error response.
    :rtype: dict or flask.Response
    """
    pass

# todo: define route for getting curated lists
@curated_picks_bp.route('/curated-lists')
@cross_origin()
@requires_auth('booklist:get')
def fetch_curated_lists(_):
    """
    Fetches curated picks.
    :return: JSON array of curated picks if the request is successful, or aborts with an error response.
    :rtype: list or flask.Response
    """
    return 'Healthy curated lists'

# todo: define route for setting curated pick
@curated_picks_bp.route('/curated-pick', methods=['POST'])
@cross_origin()
@requires_auth('booklist:curator')
def add_curated_pick(_):
    """
    Adds a curated list.
    :return: JSON object of the added curated list if the request is successful, or aborts with an error response.
    :rtype: dict or flask.Response
    """
    pass

# todo: define routes for getting curated picks
@curated_picks_bp.route('/curated-picks')
@cross_origin()
@requires_auth('booklist:get')
def fetch_curated_picks(_):
    """
    Fetches curated picks.
    :return: JSON array of curated picks if the request is successful, or aborts with an error response.
    :rtype: list or flask.Response
    """
    return 'Healthy curated picks'

