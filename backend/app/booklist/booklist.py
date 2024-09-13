from flask import (
    request,
)

from app.models.book_dto import BookDto
from app.models.book_shelf import BookShelf
from app.models.shelf import Shelf
from app.pagination.books import paginate


def booklist(used_id: str, shelf: str):

    def query():
        return (
            BookDto.query
            .join(BookShelf, BookShelf.isbn13 == BookDto.isbn13)
            .join(Shelf, Shelf.shelfID == BookShelf.shelfID)
            .filter(Shelf.shelf_name == shelf)
            .filter(Shelf.userID == used_id)
            .order_by(BookDto.title)
            .all()
        )

    return paginate(request=request, query=query)
