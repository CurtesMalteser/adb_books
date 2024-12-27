from flask import abort, jsonify, Request
from sqlalchemy import or_

from app.exceptions.invalid_request_error import InvalidRequestError
from app.models.book_dto import db
from app.models.curated_list import CuratedList, CuratedListRequest
from app.models.curated_pick import CuratedPickRequest, CuratedPick


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


def get_curated_lists():
    """
    Fetches curated picks.
    :return: JSON array of curated lists if the request is successful, or aborts with an error response.
    :rtype: lists or flask.Response
    """
    try:
        curated_lists = CuratedList.query.all()
        curated_lists = [CuratedListRequest(cl.id, cl.name, cl.description).to_dict() for cl in curated_lists]

        return jsonify({
            "success": True,
            "lists": curated_lists,
        })

    except Exception as e:
        print(f'🧨 {e}')
        abort(500)


def _get_curated_pick_request_or_throw(json: dict) -> CuratedPickRequest:
    try:
        return CuratedPickRequest.from_json(d=json)
    except Exception as e:
        raise InvalidRequestError(code=422, message=f'{e}')


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
                    CuratedPick.isbn_13 == curated_pick_request.isbn_13,
                    CuratedPick.isbn_10 == curated_pick_request.isbn_10,
                )
            ).first()

            if curated_pick is None:
                curated_pick = CuratedPick(
                    list_id=curated_pick_request.list_id,
                    isbn_13=curated_pick_request.isbn_13,
                    isbn_10=curated_pick_request.isbn_10,
                    position=curated_pick_request.position,
                )

                curated_pick.insert()
                curated_pick_request.id = curated_pick.id

                return jsonify({
                    "success": True,
                    "pick": curated_pick_request.to_dict(),
                }), 201

            else:
                print(f'❌ {curated_pick}')
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
