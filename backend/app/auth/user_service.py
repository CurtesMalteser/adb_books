from abc import ABC, abstractmethod

from app.models.user import User


class UserService(ABC):
    """Abstract interface defining the contract for user service classes."""

    @abstractmethod
    def fetch_userinfo(self, token: str) -> dict:
        """
        Abstract method implementation provides user information from an external service using the provided token.

        :param token: The authentication token to use for fetching user information.
        :type token: str
        :return: A dictionary containing user information.
        :rtype: dict
        """
        pass

    @abstractmethod
    def get_or_create_user(self, payload: dict) -> User:
        """
        Abstract method to get or create a user based on the provided payload.

        :param payload: A dictionary containing user information.
        :type payload: dict
        :return: A User object representing the user.
        :rtype: User
        """
        pass
