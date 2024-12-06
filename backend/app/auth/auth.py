import logging
from functools import wraps, lru_cache
from os import environ as env

import jwt
from dotenv import load_dotenv, find_dotenv
from flask import request
from jwt import PyJWKClient

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
    AuthError Exception
    A standardized way to communicate auth failure modes
    """

    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
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


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 403)

    return True


@lru_cache(maxsize=1)
def get_jwks_client():
    return PyJWKClient(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')


def verify_decode_jwt(token):
    jwks_client = get_jwks_client()
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


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper

    return requires_auth_decorator
