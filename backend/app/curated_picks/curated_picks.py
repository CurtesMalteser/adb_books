from flask import abort, jsonify, Request

from app.exceptions.invalid_request_error import InvalidRequestError
from app.models.book_dto import db
from app.models.curated_list import CuratedList, CuratedListRequest


def store_curated_list(request: Request):
    """
    Adds a curated list.
    :return: JSON object of the added curated list if the request is successful, or aborts with an error response.
    :rtype: dict or flask.Response
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
                    "book": curated_list_request.to_dict(),
                })

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
