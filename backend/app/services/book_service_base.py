"""
This module defines the BookServiceInterface class which is an abstract class that defines the contract for book service classes.
"""
from abc import ABC, abstractmethod
from typing import Optional

from app.models.book_shelf import BookShelf
from app.models.shelf import ShelfEnum


class BookServiceBase(ABC):
    """
    Abstract interface defining the contract for book service classes.
    """

    @abstractmethod
    def fetch_book(self, book_shelf: Optional['BookShelf'], isbn10: str | None = None,
                   isbn13: str | None = None) -> dict:
        pass

    @staticmethod
    def get_shelf_or_none(book_shelf):
        """
        Returns the shelf of a book or None if the book is not on a shelf.
        :param book_shelf:
        :return: ShelfEnum as string or None
        """
        if book_shelf is not None:
            return ShelfEnum.to_str(book_shelf.shelf)
        else:
            return None
