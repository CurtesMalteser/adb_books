from flask import (
    request,
)

from app.models.book_dto import BookDto
from app.models.book_shelf import BookShelf
from app.models.shelf import ShelfEnum
from app.pagination.books import paginate


def booklist(used_id: str, shelf: str):
    query = lambda: (
        BookDto.query
        .join(BookShelf, BookShelf.isbn13 == BookDto.isbn13)
        .filter(BookShelf.userID == used_id)
        .filter(BookShelf.shelf == ShelfEnum.from_str(shelf))
        .order_by(BookDto.title)
        .all()
    )

    return paginate(request=request, query=query)
