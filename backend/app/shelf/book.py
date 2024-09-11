from flask import abort, jsonify, Request

from app.models.book_dto import BookResponse, BookDto, db


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


# @TODO: fetch details from server or redis
def get_book(book_id: str):
    error = False
    book = None
    try:
        book_dto = BookDto.query.filter(BookDto.bookId == str(book_id)).one_or_none()
        if isinstance(book_dto, BookDto):
            # Ignore type cast because it checks if it is a BookDto
            book = Book.fromDto(book_dto)  # type: ignore
        else:
            error = True

    except Exception as ex:
        db.session.rollback()
        error = True
        print(f"🧨 error: {ex}")
    finally:
        db.session.close()

    if error:
        abort(400)
    else:
        return jsonify({
            "success": True,
            "book": book,
        })

def remove_book(book_id: str):
    try:
        book_dto = BookDto.query.filter(BookDto.bookId == book_id).one_or_none()
        if book_dto is not None: book_dto.delete()

    except:
        db.session.rollback()

    finally:
        db.session.close()

    return jsonify({
        "sucess": True,
        "deleted": book_id,
    })