"""This module defines the NYTimesServiceBase class which is an abstract class that defines the contract for NYTimes service classes."""
from abc import ABC, abstractmethod


class NYTimesServiceBase(ABC):
    """Abstract interface defining the contract for NYTimes service classes."""

    @abstractmethod
    def fetch_books(self, path: str, page: int, limit: int) -> list[dict]:
        """
        Abstract method to fetch NYTimes bestsellers.

        :param path: fiction, non-fiction, etc.
        :param page: the page number.
        :param limit: booklist response maximum size.
        :return: JSON dictionary containing the bestsellers list.
        """
        pass
