import os
from urllib.parse import urljoin
import json
import requests
from flask import abort, jsonify, Request

from app.config import GET_BOOK_ENDPOINT, REDIS_EXPIRY_TIME
from app.exceptions.invalid_request_error import InvalidRequestError

from app.models.book_dto import BookResponse, BookDto, db
from app.models.book import Book

from requests import (
    JSONDecodeError,
    RequestException,
)

from app.models.book_shelf import BookShelf
from app.models.shelf import ShelfEnum
from app.models.user import User
from app.redis_config import redis_client

api_key = os.environ.get('ISBNDB_KEY')
user_agent = os.environ.get('USER_AGENT')


def store_book(payload, request: Request):
    user_id = payload.get('sub')

    if request.is_json:
        try:
            # @TODO: Add validate token endpoint and there this code should be applied
            # Ensure the user exists or create a new one
            user = User.query.filter_by(userID=user_id).first()
            if user is None:
                user = User(
                    userID=user_id,
                    username=payload.get('name'),
                    email=payload.get('email')
                )
                db.session.add(user)

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
                    shelf=book_request.shelf
                )
                db.session.add(book)

            # Link the book to the user's shelf (BookShelf table)
            new_book_shelf = BookShelf(
                isbn13=book.isbn13,
                shelf=ShelfEnum.from_str(book.shelf),
                user_id=user_id
            )
            db.session.add(new_book_shelf)

            # Commit all changes in one go
            db.session.commit()

            return jsonify({
                "success": True,
                "book": book_request
            })

        except InvalidRequestError as e:
            abort(e.code, e.message)

        except Exception as e:
            # TODO: Define specific exceptions and use the custom error handler for 422 errors.
            print(f'🧨 {e}')
            db.session.rollback()
            abort(422)

        finally:
            db.session.close()

    else:
        abort(404, "Content type is not supported.")


def get_book(book_id: str):
    """
    :param book_id: ISBN13
    :type book_id: str

    :return: Book if the request is successful, or aborts with an error response.
    :rtype: flask.Response
    """

    url = urljoin(GET_BOOK_ENDPOINT, book_id)

    headers = {
        "User-Agent": user_agent,
        "Authorization": api_key
    }

    try:
        book = redis_client.get(book_id)

        if book is None:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            json_response = response.json().get('book')

            book = Book.from_json(d=json_response).to_dict()
            redis_client.set(book_id, json.dumps(book), ex=REDIS_EXPIRY_TIME)

        else:
            book = json.loads(book)

        return jsonify(
            {
                "success": True,
                "book": book,
            }
        )

    except JSONDecodeError:
        abort(500, description="Invalid JSON response from upstream server.")

    except RequestException as e:
        abort(500, description=f"An error occurred while fetching data: {str(e)}")


def remove_book(book_id: str):
    try:
        book_dto = BookDto.query.filter(BookDto.bookId == book_id).one_or_none()
        if book_dto is not None: book_dto.delete()

    except:
        db.session.rollback()

    finally:
        db.session.close()

    return jsonify({
        "success": True,
        "deleted": book_id,
    })


def update_book_shelf(user_id: str, book_id: str, request: Request):
    try:
        if request.is_json:
            book_shelf = BookShelf.query.filter_by(
                isbn13=book_id,
                userID=user_id
            ).one_or_none()

            if book_shelf is not None:
                shelf = ShelfEnum.from_str(request.get_json().get('shelf'))
                book_shelf.shelf = shelf
                db.session.add(book_shelf)
                db.session.commit()

                return jsonify({
                    "success": True,
                    "error": 200
                })
            else:
                raise InvalidRequestError(code=409,
                                          message=f'Shelf not found for the given user and ISBN-13. Try add to shelf first')

    except InvalidRequestError as e:
        raise e

    except Exception as e:
        print(f'🧨 {e}')
        db.session.rollback()
        abort(422)

    finally:
        db.session.close()
