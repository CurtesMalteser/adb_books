import inject
from flask import abort, jsonify, Request
from sqlalchemy import or_

from app.exceptions.invalid_request_error import InvalidRequestError
from app.models.book_dto import db
from app.models.curated_list import CuratedList, CuratedListRequest
from app.models.curated_pick import CuratedPickRequest, CuratedPick
from app.services.book_service_base import BookServiceBase
from app.utils.isbn_utils import is_valid_isbn


def store_curated_list(request: Request):
    """
    Adds a curated list.
    :return: JSON object of the added curated list if the request is successful, or aborts with an error response.
    :rtype: list or flask.Response
    """
    try:
        if request.is_json:
            curated_list_request = CuratedListRequest.from_json(d=request.get_json())
            curated_list = CuratedList.query.filter_by(name=curated_list_request.name).first()

            if curated_list is None:
                curated_list = CuratedList(
                    name=curated_list_request.name,
                    description=curated_list_request.description,
                )

                curated_list.insert()
                curated_list_request.id = curated_list.id

                return jsonify({
                    "success": True,
                    "list": curated_list_request.to_dict(),
                }), 201

            else:
                message = f'Curated list \'{curated_list.name}\' already exists, Try PUT to update.'
                raise InvalidRequestError(code=409, message=message)
        else:
            raise InvalidRequestError(code=404, message='Content type is not supported.')

    except InvalidRequestError as e:
        raise e

    except Exception as e:
        # TODO: Reraise specific exceptions and use the custom error handler for 422 errors.
        print(f'🧨 {e}')
        db.session.rollback()
        abort(422)


def store_curated_list_update(request: Request):
    """
    Updates a curated list.
    :param request:
    :type request: Request
    :return: updated curated list JSON object if the request is successful, or aborts with an error response.
    """
    try:
        if request.is_json:
            curated_list_request = CuratedListRequest.from_json(d=request.get_json())
            curated_list = CuratedList.query.filter_by(id=curated_list_request.id).first()

            if curated_list is not None:
                curated_list.name = curated_list_request.name
                curated_list.description = curated_list_request.description

                curated_list.update()

                return jsonify({
                    "success": True,
                    "list": curated_list_request.to_dict(),
                }), 200

            else:
                message = f'Curated list with ID \'{curated_list_request.id}\' does not exist.'
                raise InvalidRequestError(code=404, message=message)

        else:
            raise InvalidRequestError(code=404, message='Content type is not supported.')
    except InvalidRequestError as e:
        raise e


def delete_curated_list_by_id(list_id: int):
    """
    Deletes a curated list by ID.
    :param list_id: ID of the curated list to delete.
    :type list_id: int
    :return: 204 status code if the request is successful, or aborts with an error response.
    :rtype: dict or flask.Response
    """
    try:
        curated_list = db.session.get(CuratedList, list_id)

        if curated_list:
            curated_list.delete()
            return "", 204  # RESTful standard for successful DELETE

        else:
            raise InvalidRequestError(code=404, message='The specified list does not exist.')

    except InvalidRequestError as e:
        raise e

    except Exception as e:
        print(f'🧨 {e}')
        db.session.rollback()
        abort(500)


def get_curated_lists():
    """
    Fetches curated picks.
    :return: JSON array of curated lists if the request is successful, or aborts with an error response.
    :rtype: lists or flask.Response
    """
    try:
        curated_lists = CuratedList.query.all()
        curated_lists = [CuratedListRequest(id=cl.id, name=cl.name, description=cl.description).to_dict() for cl in
                         curated_lists]

        return jsonify({
            "success": True,
            "lists": curated_lists,
        })

    except Exception as e:
        print(f'🧨 {e}')
        abort(500)


def store_curated_pick(request: Request):
    """
    Adds a curated pick.
    :return: JSON object of the added curated pick if the request is successful, or aborts with an error response.
    :rtype: dict or flask.Response
    """
    try:
        if request.is_json:
            curated_pick_request = _get_curated_pick_request_or_throw(request.get_json())
            pick_id = curated_pick_request.isbn13 or curated_pick_request.isbn10
            curated_pick = _get_pick_by_isbn(pick_id=pick_id)
            if curated_pick is None:
                curated_pick = CuratedPick(
                    list_id=curated_pick_request.list_id,
                    isbn13=curated_pick_request.isbn13,
                    isbn10=curated_pick_request.isbn10,
                    position=curated_pick_request.position,
                )

                curated_pick.insert()
                curated_pick_request.id = curated_pick.id

                return jsonify({
                    "success": True,
                    "pick": curated_pick_request.to_dict(),
                }), 201

            else:
                message = f'Curated pick \'{curated_pick}\' already exists, Try PUT to update.'
                raise InvalidRequestError(code=409, message=message)

        else:
            raise InvalidRequestError(code=404, message='Content type is not supported.')

    except InvalidRequestError as e:
        raise e

    except Exception as e:
        # TODO: Reraise specific exceptions and use the custom error handler for 422 errors.
        print(f'🧨 {e}')
        db.session.rollback()
        abort(422)


def delete_curated_pick_by_id(pick_id: str):
    """
    Deletes a curated pick by ID.
    :param pick_id: ID of the curated pick to delete.
    :type pick_id: str, expected an ISBN10 or ISBN13
    :return: 204 status code if the request is successful, or aborts with an error response.
    :rtype: flask.Response
    """
    try:
        return _delete_pick_by_id(pick_id)
    except InvalidRequestError as e:
        raise e

    except Exception as e:
        print(f'🧨 {e}')
        db.session.rollback()
        abort(500)


def update_curated_pick_position(pick_id: str, request: Request):
    """
    Updates a curated pick.
    :param pick_id: ID of the curated pick to update.
    :type pick_id: str, expected an ISBN10 or ISBN13
    :param request: Request object
    :type request: Request
    :return: JSON object of the updated curated pick if the request is successful, or aborts with an error response.
    :rtype: flask.Response
    """
    try:
        if request.is_json:
            new_position = request.get_json().get('position')
            return _update_pick_position(pick_id=pick_id, new_position=new_position)

    except InvalidRequestError as e:
        raise e

    except Exception as e:
        print(f'🧨 {e}')
        db.session.rollback()
        abort(422)


@inject.params(book_service=BookServiceBase)
def get_curated_picks(list_id_func: callable, book_service: BookServiceBase):
    """
    Fetches curated picks.
    :return: JSON array of curated lists if the request is successful, or aborts with an error response.
    :rtype: lists or flask.Response
    """
    try:
        if list_id := list_id_func():
            _validate_list_exist_or_404(list_id)

            curated_picks = CuratedPick.query.filter_by(list_id=list_id).all()

            json_books = []
            for cp in curated_picks:
                book = book_service.fetch_book(None, isbn10=cp.isbn10, isbn13=cp.isbn13)
                book["position"] = cp.position
                if book:  # Ensure book data is valid
                    json_books.append(book)

        else:
            raise InvalidRequestError(code=404, message='List ID is required.')

        return jsonify(
            {
                'success': True,
                'books': list(json_books),
                'page': 1,
                'limit': len(json_books),
                'total_results': len(json_books)
            }
        )

    except InvalidRequestError as e:
        raise e

    except Exception as e:
        print(f'🧨 {e}')
        abort(500)


def _get_curated_pick_request_or_throw(json: dict) -> CuratedPickRequest:
    try:
        return CuratedPickRequest.from_json(d=json)
    except Exception as e:
        raise InvalidRequestError(code=422, message=f'{e}')


def _validate_list_exist_or_404(list_id):
    curated_list = db.session.get(CuratedList, list_id)
    if not curated_list:
        raise InvalidRequestError(code=404, message="The specified list does not exist.")


def _delete_pick_by_id(pick_id: str):
    """
    Returns the book ID based on the ISBN provided.
    """
    if is_valid_isbn(isbn10=pick_id, isbn13=pick_id):
        curated_pick = _get_pick_by_isbn(pick_id=pick_id)
        if curated_pick:
            curated_pick.delete()
            return "", 204  # RESTful standard for successful DELETE
        else:
            raise InvalidRequestError(code=404, message=f"The specified pick ID:'{pick_id}' does not exist.")
    else:
        raise InvalidRequestError(code=404, message=f"Incorrect pick ID format:'{pick_id}'. ISBN10 or ISBN13 expected.")


def _update_pick_position(pick_id: str, new_position: int):
    """
    Updates the position of a curated pick.
    Adjusts other picks in the range between the current and new positions.
    :param pick_id: The ID of the pick (ISBN).
    :param new_position: The new position for the pick.
    :return: JSON response indicating success.
    """
    # Validate the new position
    if new_position < 1:
        raise InvalidRequestError(code=400, message="Invalid position value.")

    # Fetch the target pick
    target_pick = _get_pick_by_isbn(pick_id=pick_id)
    if not target_pick:
        raise InvalidRequestError(code=404, message=f"The specified pick ID:'{pick_id}' does not exist.")

    current_position = target_pick.position
    if current_position == new_position:
        # No changes needed
        return jsonify({"success": True, "pick": CuratedPickRequest.from_model(target_pick).to_dict()})

    is_moving_up = new_position < current_position

    # Use a placeholder to avoid conflicts
    placeholder_position = -1
    target_pick.position = placeholder_position
    target_pick.update()

    # Fetch only affected picks
    affected_picks_query = CuratedPick.query.filter(CuratedPick.list_id == target_pick.list_id)

    if is_moving_up:
        affected_picks_query = affected_picks_query.filter(
            CuratedPick.position >= new_position, CuratedPick.position < current_position
        ).order_by(CuratedPick.position.desc())  # Process from bottom to top
    else:
        affected_picks_query = affected_picks_query.filter(
            CuratedPick.position > current_position, CuratedPick.position <= new_position
        ).order_by(CuratedPick.position.asc())  # Process from top to bottom

    affected_picks = affected_picks_query.all()

    # Update affected picks sequentially
    for pick in affected_picks:
        pick.position += 1 if is_moving_up else -1
        pick.update()

    # Update the target pick position
    target_pick.position = new_position
    target_pick.update()

    # Commit all changes
    db.session.commit()

    try:
        json = CuratedPickRequest.from_model(target_pick).to_dict()
    except Exception as e:
        raise InvalidRequestError(code=500, message=str(e))

    return jsonify({
        "success": True,
        "pick": json
    })


def _get_pick_by_isbn(pick_id):
    """
    Returns a CuratedPick object based on the ISBN provided.
    :param pick_id: ISBN10 or ISBN13
    :return: CuratedPick object or None
    """
    return CuratedPick.query.filter(
        or_(CuratedPick.isbn13 == pick_id, CuratedPick.isbn10 == pick_id)
    ).first()
