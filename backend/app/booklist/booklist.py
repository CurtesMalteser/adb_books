from flask import (
    request,
)

from app.models.book_dto import BookDto
from app.models.book_shelf import BookShelf
from app.models.shelf import Shelf
from app.pagination.books import paginate


def booklist(shelf: str):
    # TODO: get uid from Bearer token
    userID = 'random_id'

    def query():
        return (
            BookDto.query
            .join(BookShelf, BookShelf.isbn13 == BookDto.isbn13)
            .join(Shelf, Shelf.shelfID == BookShelf.shelfID)
            .filter(Shelf.shelf_name == shelf)
            .filter(Shelf.userID == userID)
            .order_by(BookDto.title)
            .all()
        )

    return paginate(request=request, query=query)
