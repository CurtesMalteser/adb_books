"""
This module defines the AuthInterface class which is an abstract class that defines the contract for authentication classes.
"""
from abc import ABC, abstractmethod


class AuthInterface(ABC):
    """
    Abstract interface defining the contract for authentication classes.
    """

    @abstractmethod
    def validate_token(self, permission: str):
        pass
