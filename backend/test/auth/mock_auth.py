import json

from flask import request

from app.auth.auth import AuthError
from app.auth.auth_interface import AuthInterface


class MockAuth(AuthInterface):

    def validate_token(self, permission: str):
        payload = self._get_token_auth_header()
        self._check_permissions(permission, payload)
        return payload

    def _get_token_auth_header(self):
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

        json_token = auth.removeprefix("Bearer ").strip()
        return json.loads(json_token)

    def _check_permissions(self, permission, payload):
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
