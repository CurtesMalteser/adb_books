"""This module provides an implementation of UserService for Auth0 users."""
from os import environ as env

import requests
from flask import request

from app.auth.user_service import UserService
from app.models.user import User

# or from your models root
AUTH0_DOMAIN = env.get('AUTH0_DOMAIN')


class Auth0UserService(UserService):
    """Concrete implementation of UserService for Auth0 users."""

    def fetch_userinfo(self, token):
        resp = requests.get(
            f'https://{AUTH0_DOMAIN}/userinfo',
            headers={"Authorization": f"Bearer {token}"}
        )
        return resp.json() if resp.ok else {}

    def get_or_create_user(self, payload):
        user_id = payload.get("sub")
        user = User.query.filter_by(userID=user_id).first()

        if user:
            return user

        # fallback values
        username = payload.get("name")
        email = payload.get("email")

        if not username or not email:
            token = request.headers.get("Authorization", "").replace("Bearer ", "")
            userinfo = self.fetch_userinfo(token)
            username = username or userinfo.get("nickname", "unknown")
            email = email or userinfo.get("email", "unknown@example.com")

        new_user = User(userID=user_id, username=username, email=email)
        new_user.insert()
        return new_user
