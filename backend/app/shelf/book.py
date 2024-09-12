import os
from urllib.parse import urljoin
import json
import requests
from flask import abort, jsonify, Request

from app.config import GET_BOOK_ENDPOINT, REDIS_EXPIRY_TIME

from app.models.book_dto import BookResponse, BookDto, db
from app.models.book import Book

from requests import (
    JSONDecodeError,
    RequestException,
)

from app.redis_config import redis_client

api_key = os.environ.get('ISBNDB_KEY')
user_agent = os.environ.get('USER_AGENT')


def store_book(request: Request):
    if request.is_json:
        try:
            book_request = BookResponse.from_json(d=request.get_json())
            book = BookDto.query.filter(BookDto.isbn13 == book_request.isbn13).one_or_none()

            if book is None:
                BookDto(isbn13=book_request.isbn13,
                        title=book_request.title,
                        authors=book_request.authors,
                        shelf=book_request.shelf,
                        image=book_request.image).insert()

            return jsonify({
                "success": True,
                "book": book_request
            })

        # TODO: Define specific exceptions and use the custom error handler for 422 errors.
        except:
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
