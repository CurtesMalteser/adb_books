"""This module provides an implementation of UserService for Auth0 users."""
from os import environ as env

import requests
from flask import request

from app.auth.user_service import UserService
from app.exceptions.invalid_request_error import InvalidRequestError
from app.models.user import User

# or from your models root
AUTH0_DOMAIN = env.get('AUTH0_DOMAIN')


class Auth0UserService(UserService):
    """Concrete implementation of UserService for Auth0 users."""

    def fetch_userinfo(self, token) -> dict:
        """Fetches user information from Auth0 using the provided token."""
        resp = requests.get(
            f'https://{AUTH0_DOMAIN}/userinfo',
            headers={"Authorization": f"{token}"}
        )
        return resp.json() if resp.ok else {}

    def get_or_create_user(self, payload) -> User:
        """Gets or creates a user based on the provided payload.

        This method checks if the user already exists in the database.
        If the user does not exist, it fetches user information from Auth0 using the provided token,

        :param payload: A dictionary containing user information.
        :type payload: dict
        :return: A User object representing the user.
        :rtype: User
        """
        user_id = payload.get("sub")
        user = User.query.filter_by(userID=user_id).first()
        print(f"User found: {user}")

        if user:
            return user

        token = request.headers.get("Authorization", "")
        userinfo = self.fetch_userinfo(token)
        email_verified = userinfo.get("email_verified", False)
        print(f"Userinfo: {userinfo}")

        if not email_verified:
            raise InvalidRequestError(401, "Email not verified")

        username = userinfo.get("nickname", None)
        email = userinfo.get("email", None)

        if not username or not email:
            raise InvalidRequestError(401, "Username or email not found in userinfo")

        try:
            new_user = User(userID=user_id, username=username, email=email)
            new_user.insert()

            return new_user

        except Exception as e:
            raise InvalidRequestError(500, f"Failed to create user: {str(e)}")
