"""This module defines the BookServiceInterface class which is an abstract class that defines the contract for book service classes."""
from abc import ABC, abstractmethod
from typing import Optional

from app.models.book_shelf import BookShelf
from app.models.shelf import ShelfEnum


class BookServiceBase(ABC):
    """Abstract interface defining the contract for book service classes."""

    @abstractmethod
    def fetch_book(
            self,
            book_shelf: Optional['BookShelf'],
            isbn10: str | None = None,
            isbn13: str | None = None
    ) -> dict:
        """
        Abstract method to fetch book details.

        This method must be implemented by subclasses to retrieve book information
        based on the provided ISBN-10 or ISBN-13 and the associated BookShelf object.

        :param book_shelf: Optional BookShelf object containing shelf information.
        :type book_shelf: Optional[BookShelf]
        :param isbn10: ISBN-10 identifier of the book (optional).
        :type isbn10: str | None
        :param isbn13: ISBN-13 identifier of the book (optional).
        :type isbn13: str | None
        :return: A dictionary containing the book details.
        :rtype: dict
        """
        pass

    @abstractmethod
    def search_books(self, query: str, page: int, limit: int) -> dict:
        """
        Abstract method to search for books based on a query.

        This method must be implemented by subclasses to perform a search for books
        based on the provided query string, page number, and limit.

        :param query: The search query string.
        :type query: str
        :param page: The page number for paginated results.
        :type page: int
        :param limit: The number of results per page.
        :type limit: int
        :return: A dictionary containing the search results, including success status, books, page, limit, and total results.
        :rtype: dict
        """
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
