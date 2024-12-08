"""
This module is used to configure the dependency injection for the application.
"""
import inject
from inject import Binder

from app.auth.auth import Auth
from app.auth.auth_interface import AuthInterface


def configure_dependencies(binder: Binder):
    """
    Configure the dependencies for the application
    :param binder:
    """
    binder.bind_to_provider(AuthInterface, Auth)


def initialize_di():
    """
    Initialize the dependency injection for the application
    """
    inject.configure_once(configure_dependencies)
