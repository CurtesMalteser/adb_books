from flask import Blueprint, request, abort
from flask_cors import cross_origin

from app.auth.auth import requires_auth
from app.curated_picks.curated_picks import (store_curated_list,
                                             get_curated_lists,
                                             store_curated_pick,
                                             get_curated_picks,
                                             store_curated_list_update,
                                             delete_curated_list_by_id,
                                             delete_curated_pick_by_id,
                                             )

curated_picks_bp = Blueprint('curated_picks', __name__)


@curated_picks_bp.route('/curated-list', methods=['POST'])
@cross_origin()
@requires_auth('booklist:curator')
def add_curated_list(_):
    """
    Adds a curated list.
    :return: JSON object of the added curated list if the request is successful, or aborts with an error response.
    :rtype: dict or flask.Response
    """
    return store_curated_list(request=request)


@curated_picks_bp.route('/curated-list', methods=['PUT'])
@cross_origin()
@requires_auth('booklist:curator')
def update_curated_list(_):
    """
    Adds a curated list.
    :return: JSON object of the added curated list if the request is successful, or aborts with an error response.
    :rtype: dict or flask.Response
    """
    return store_curated_list_update(request=request)


@curated_picks_bp.route('/curated-list/<int:list_id>', methods=['DELETE'])
@cross_origin()
@requires_auth('booklist:curator')
def delete_curated_list(_, list_id: int):
    """
    Adds a curated list.
    :return: JSON object of the added curated list if the request is successful, or aborts with an error response.
    :rtype: dict or flask.Response
    """
    return delete_curated_list_by_id(list_id)


@curated_picks_bp.route('/curated-lists')
@cross_origin()
@requires_auth('booklist:get')
def fetch_curated_lists(_):
    """
    Fetches curated picks.
    :return: JSON array of curated picks if the request is successful, or aborts with an error response.
    :rtype: list or flask.Response
    """
    return get_curated_lists()


@curated_picks_bp.route('/curated-pick', methods=['POST'])
@cross_origin()
@requires_auth('booklist:curator')
def add_curated_pick(_):
    """
    Adds a curated list.
    :return: JSON object of the added curated list if the request is successful, or aborts with an error response.
    :rtype: dict or flask.Response
    """
    return store_curated_pick(request=request)


@curated_picks_bp.route('/curated-pick', methods=['PUT'])
@cross_origin()
@requires_auth('booklist:curator')
def update_curated_pick(_):
    """
    Adds a curated list.
    :return: JSON object of the added curated list if the request is successful, or aborts with an error response.
    :rtype: dict or flask.Response
    """
    abort(501)


@curated_picks_bp.route('/curated-pick/<string:list_id>', methods=['DELETE'])
@cross_origin()
@requires_auth('booklist:curator')
def delete_curated_pick(_, list_id: str):
    """
    Adds a curated list.
    :return: JSON object of the added curated list if the request is successful, or aborts with an error response.
    :rtype: dict or flask.Response
    """

    return delete_curated_pick_by_id(list_id)


@curated_picks_bp.route('/curated-picks')
@cross_origin()
@requires_auth('booklist:get')
def fetch_curated_picks(_):
    """
    Fetches curated picks.
    :return: JSON array of curated picks if the request is successful, or aborts with an error response.
    :rtype: list or flask.Response
    """
    return get_curated_picks(lambda: request.args.get('list_id', type=int))
