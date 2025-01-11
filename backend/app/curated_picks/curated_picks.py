import inject
from flask import abort, jsonify, Request
from sqlalchemy import or_

from app.exceptions.invalid_request_error import InvalidRequestError
from app.models.book_dto import db
from app.models.curated_list import CuratedList, CuratedListRequest
from app.models.curated_pick import CuratedPickRequest, CuratedPick
from app.services.book_service_base import BookServiceBase


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

    finally:
        db.session.close()


def store_curated_list_update(request: Request):
    """
    Updates a curated list.
    :param request:
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
            curated_pick = CuratedPick.query.filter(
                or_(
                    CuratedPick.isbn13 == curated_pick_request.isbn13,
                    CuratedPick.isbn10 == curated_pick_request.isbn10,
                )
            ).first()

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


    finally:
        db.session.close()


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
    curated_list = CuratedList.query.get(list_id)
    if not curated_list:
        raise InvalidRequestError(code=404, message="The specified list does not exist.")
