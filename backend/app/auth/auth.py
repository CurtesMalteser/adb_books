"""Authentication and authorization using JWT for the Flask API.

This module defines the Auth class, which implements token validation,
permission checking, and JWT verification using Auth0 and PyJWT.

It also provides the `requires_auth` decorator to protect endpoints
based on role permissions (RBAC).

Environment variables required:
- AUTH0_DOMAIN
- API_AUDIENCE
"""
import logging
from functools import wraps, lru_cache
from os import environ as env

import jwt
from dotenv import load_dotenv, find_dotenv
from flask import request
from jwt import PyJWKClient

from app.auth.auth_interface import AuthInterface

"""
This module is used to configure the dependency injection for the application.
"""
import inject

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

AUTH0_DOMAIN = env.get('AUTH0_DOMAIN')
API_AUDIENCE = env.get('API_AUDIENCE')
ALGORITHMS = ['RS256']

# Logger setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class AuthError(Exception):
    """
    Custom exception for authentication and authorization errors.

    Used to standardize error responses when token validation or permission checks fail.
    """
    def __init__(self, error, status_code):
        """
        Initializes the AuthError with an error message and status code.

        :param error:
        :param status_code:
        """
        self.error = error
        self.status_code = status_code


class Auth(AuthInterface):
    """
    Concrete implementation of AuthInterface using Auth0 and PyJWT.

    Provides methods to:
    - Extract and validate bearer tokens from requests
    - Check permissions within the token payload
    - Decode and verify tokens against Auth0's public keys
    """

    def validate_token(self, permission):
        """
        Validates the token in the request and checks required permission.

        :param permission: Required permission (e.g., 'read:books')
        :return: Decoded token payload if valid
        :raises AuthError: If token is invalid or permission is missing
        """
        token = self._get_token_auth_header()
        payload = self._verify_decode_jwt(token)
        self._check_permissions(permission, payload)
        return payload

    def _get_token_auth_header(self):
        """
        Extracts the bearer token from the Authorization header.

        :return: Raw JWT token string
        :raises AuthError: If header is missing or improperly formatted
        """
        auth = request.headers.get('Authorization', None)

        if not auth:
            raise AuthError({
                'code': 'authorization_header_missing',
                'description': 'Authorization header is expected.'
            }, 401)

        parts = auth.split()

        if parts[0].lower() != 'bearer':
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Authorization header must start with "Bearer".'
            }, 401)

        if len(parts) == 1:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Token not found.'
            }, 401)

        if len(parts) > 2:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Authorization header must be bearer token.'
            }, 401)

        return parts[1]

    def _check_permissions(self, permission, payload):
        """
        Checks if the permission exists in the JWT payload.

        :param permission: Required permission string
        :param payload: Decoded JWT payload
        :raises AuthError: If permission is missing or claims are invalid
        """
        if 'permissions' not in payload:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Permissions not included in JWT.'
            }, 400)

        if permission not in payload['permissions']:
            raise AuthError({
                'code': 'forbidden',
                'description': 'Permission not found.'
            }, 403)

        return True

    @lru_cache(maxsize=1)
    def _get_jwks_client(self):
        """
        Returns a cached PyJWKClient for fetching Auth0's public keys.

        :return: PyJWKClient instance
        """
        return PyJWKClient(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')

    def _verify_decode_jwt(self, token):
        """
        Decodes and verifies a JWT token using Auth0's public keys.

        :param token: Encoded JWT string
        :return: Decoded payload dictionary
        :raises AuthError: On token expiration, format errors, or verification failure
        """
        jwks_client = self._get_jwks_client()
        signing_key = jwks_client.get_signing_key_from_jwt(token)

        try:
            payload = jwt.decode(
                token,
                signing_key.key,  # Use the key property
                audience=API_AUDIENCE,
                algorithms=["RS256"],
            )
            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token has expired.'
            }, 401)
        except jwt.InvalidAudienceError:
            raise AuthError({
                'code': 'invalid_audience',
                'description': 'Incorrect audience in the token.'
            }, 401)
        except jwt.InvalidIssuerError:
            raise AuthError({
                'code': 'invalid_issuer',
                'description': 'Incorrect issuer in the token.'
            }, 401)
        except jwt.ImmatureSignatureError:
            raise AuthError({
                'code': 'token_not_yet_valid',
                'description': 'Token is not yet valid (nbf claim).'
            }, 401)
        except jwt.DecodeError:
            raise AuthError({
                'code': 'decode_error',
                'description': 'Token is malformed or corrupted.'
            }, 401)
        except Exception as e:
            logger.error(f"Unexpected error during JWT decoding: {e}")
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400) from e


def requires_auth(permission: str):
    """
    Decorator to enforce role-based access on protected endpoints.

    :param permission: The permission required to access the route
    :return: Wrapped function that checks authorization before executing
    """
    def requires_auth_decorator(f):
        """
        Decorator function that wraps the original function.

        :param f:
        :return:
        """
        @wraps(f)
        def wrapper(*args, **kwargs):
            """
            Wrapper function that checks the token and permissions.

            :param args:
            :param kwargs:
            :return:
            """
            payload = inject.instance(AuthInterface).validate_token(permission)
            return f(payload, *args, **kwargs)

        return wrapper

    return requires_auth_decorator
