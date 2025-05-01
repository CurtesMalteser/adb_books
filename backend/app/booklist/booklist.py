"""
This module contains the logic for the booklist endpoint.
"""
from flask import request

from app.models.book_dto import BookDto
from app.models.book_shelf import BookShelf
from app.models.shelf import ShelfEnum
from app.pagination.books import paginate


def booklist(used_id: str, shelf: str):
    """
    Fetches a booklist by shelf type.
    :param used_id:
    :param shelf:
    :return: paginated list of books
    :rtype: flask.Response or None
    """

    def query():
        return (
        BookDto.query
        .join(BookShelf, BookShelf.isbn13 == BookDto.isbn13)
        .filter(BookShelf.userID == used_id)
        .filter(BookShelf.shelf == ShelfEnum.from_str(shelf))
        .order_by(BookDto.title)
        .all()
    )

    return paginate(request=request, query=query)
