from app.auth.user_service import UserService
from app.models.user import User


class MockUserService(UserService):
    """Mock implementation of UserService for testing purposes."""

    def fetch_userinfo(self, token: str) -> dict:
        """Intentionally left blank for mocking purposes."""
        return {}

    def get_or_create_user(self, payload: dict) -> User:
        """Returns a mock user based on the provided payload."""
        user_id = payload.get("sub")
        user = User.query.filter_by(userID=user_id).first()
        if user is None:
            new_user = User(
                userID=user_id,
                email=payload.get("email", None),
                username=payload.get("name", None)
            )
            new_user.insert()
            return new_user
        else:
            return user
