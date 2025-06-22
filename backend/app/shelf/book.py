"""
This module provides functions for managing books in a user's shelf.

It includes operations such as adding, fetching, removing, and updating books in the shelf.
These functions are used in the `shelf_bp` Blueprint to handle API requests related to book management.
"""
import os

import inject
from flask import abort, jsonify, Request
from requests import (
    JSONDecodeError,
    RequestException,
)

from app.auth.user_service import UserService
from app.exceptions.invalid_request_error import InvalidRequestError
from app.models.book_dto import BookResponse, BookDto, db
from app.models.book_shelf import BookShelf
from app.models.shelf import ShelfEnum
from app.services.book_service_base import BookServiceBase

api_key = os.environ.get('ISBNDB_KEY')
user_agent = os.environ.get('USER_AGENT')


@inject.params(user_service=UserService)
def store_book(payload, request: Request, user_service: UserService):
    """
    Stores a book in the user's shelf.

    :param payload:
    :param request:
    :param user_service: UserService instance provided by the dependency injector
    :type user_service: UserService
    :return: Book if the request is successful, or aborts with an error response.
    :rtype: flask.Response
    """
    user_id = payload.get('sub')

    if request.is_json:
        try:
            # @TODO: Add validate token endpoint and there this code should be applied
            # Ensure the user exists or create a new one
            user = user_service.get_or_create_user(payload)
            if user is None:
                raise InvalidRequestError(401, "User not found or not authenticated.")

            # Deserialize the incoming book request
            book_request = BookResponse.from_json(d=request.get_json())

            # Check if the book is already linked to the user's shelf
            book_shelf = BookShelf.query.filter_by(
                isbn13=book_request.isbn13,
                userID=user_id
            ).first()

            if book_shelf is not None:
                # If book is already on the user's shelf, raise a conflict
                raise InvalidRequestError(409, f'Book already in shelf {book_request.shelf}. Please use PATCH instead.')

            # Now check if the book exists in the BookDto table
            book = BookDto.query.filter_by(isbn13=book_request.isbn13).first()
            if book is None:
                # Insert the book if it doesn't exist
                book = BookDto(
                    isbn13=book_request.isbn13,
                    title=book_request.title,
                    authors=book_request.authors,
                    image=book_request.image,
                )

                book.insert()

            # Link the book to the user's shelf (BookShelf table)
            BookShelf(
                isbn13=book.isbn13,
                shelf=ShelfEnum.from_str(book_request.shelf),
                user_id=user_id
            ).insert()

            return jsonify({
                "success": True,
                "book": book_request.to_dict()
            })

        except InvalidRequestError as e:
            abort(e.code, e.message)

        except Exception as e:
            # TODO: Define specific exceptions and use the custom error handler for 422 errors.
            print(f'🧨 {e}')
            db.session.rollback()
            abort(422)

    else:
        abort(404, "Content type is not supported.")


@inject.params(book_service=BookServiceBase)
def get_book(user_id: str, book_id: str, book_service: BookServiceBase):
    """
    Fetches a book from the BookServiceBase using the provided user ID and book ID (ISBN13).

    :param user_id: User ID obtained from the JWT token
    :type user_id: str

    :param book_id: ISBN13
    :type book_id: str

    :param book_service: BookServiceBase instance provided by the dependency injector
    :type book_service: BookServiceBase

    :return: Book if the request is successful, or aborts with an error response.
    :rtype: flask.Response
    """
    try:
        book_shelf: BookShelf = BookShelf.get_or_none(book_id, user_id)

        book_dict = book_service.fetch_book(book_shelf, isbn13=book_id, isbn10=book_id)

        return jsonify(
            {
                "success": True,
                "book": book_dict,
            }
        )

    except JSONDecodeError:
        abort(500, description="Invalid JSON response from upstream server.")

    except RequestException as e:
        abort(500, description=f"An error occurred while fetching data: {str(e)}")


def remove_book(user_id: str, book_id: str):
    """
    Removes a book from the user's shelf.

    :param user_id:
    :param book_id:
    :return: success json response, or aborts with an error response.
    :rtype: flask.Response
    """
    try:
        book_shelf = BookShelf.get_or_none(book_id=book_id, user_id=user_id)

        if book_shelf is None:
            abort(404)

        db.session.delete(book_shelf)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        print(f"🧨 {e}")
        abort(500)

    return jsonify({
        "success": True,
        "deleted": book_id,
    })


def update_book_shelf(user_id: str, book_id: str, request: Request):
    """
    Updates the shelf for a given book and user.

    :param user_id: User ID obtained from the JWT token
    :type user_id: str
    :param book_id: ISBN13 of the book from path parameter
    :type book_id: str
    :param request: Request object which contains the JSON payload "shelf"
    :type request: Request

    :return: response object
    :rtype: flask.Response
    """
    try:
        if not request.is_json:
            abort(400, description="Invalid content type. Expected JSON.")

        book_shelf = BookShelf.get_or_none(book_id, user_id)

        if not book_shelf:
            raise InvalidRequestError(
                code=409,
                message="Shelf not found for the given user and ISBN-13. Try adding to shelf first."
            )

        shelf = ShelfEnum.from_str(request.get_json().get('shelf'))
        book_shelf.shelf = shelf
        db.session.commit()  # no need to db.session.add(book_shelf), SQLAlchemy tracks it

        return jsonify({"success": True})

    except InvalidRequestError:
        raise

    except Exception as e:
        print(f"🧨 {e}")
        db.session.rollback()
        abort(422)
