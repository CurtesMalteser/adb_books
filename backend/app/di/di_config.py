"""This module is used to configure the dependency injection for the application."""
import inject
from inject import Binder

from app.auth.auth import Auth
from app.auth.auth0_user_service import Auth0UserService
from app.auth.auth_interface import AuthInterface
from app.auth.user_service import UserService
from app.redis_config import redis_client
from app.services.book_service import BookService
from app.services.book_service_base import BookServiceBase
from app.services.ny_times_service import NyTimesService
from app.services.ny_times_service_base import NYTimesServiceBase


def create_book_service() -> BookServiceBase:
    """
    Create the BookService instance with the Redis client.

    Allows lazy loading of the BookService instance.
    :return: implementation of BookServiceBase
    """
    return BookService(redis_client)


def create_nyt_book_service() -> NYTimesServiceBase:
    """
    Create the BookService instance with the Redis client.

    Allows lazy loading of the BookService instance.
    :return: implementation of BookServiceBase
    """
    return NyTimesService(redis_client)


def create_user_service() -> UserService:
    """
    Create the UserService instance.

    Allows lazy loading of the UserService instance.
    :return: implementation of UserService
    """
    return Auth0UserService()

def configure_dependencies(binder: Binder):
    """
    Configure the dependencies for the application.

    :param binder:
    """
    binder.bind_to_provider(AuthInterface, Auth)
    binder.bind_to_provider(UserService, lambda: create_user_service())
    binder.bind_to_provider(BookServiceBase, lambda: create_book_service())
    binder.bind_to_provider(NYTimesServiceBase, lambda: create_nyt_book_service())


def initialize_di():
    """Initialize the dependency injection for the application."""
    inject.configure_once(configure_dependencies)
