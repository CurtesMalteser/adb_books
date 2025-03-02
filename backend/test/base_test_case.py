# Makes book_managment_api module available,
# if test_book_managment_api.py run from test dir, since the scriptpath is a relative path.
import json
import os
import sys
import unittest

import inject

from app import create_app
from app.auth.auth_interface import AuthInterface
from app.models.book_dto import db
from app.services.book_service_base import BookServiceBase
from test.auth.mock_auth import MockAuth
from test.services.mock_book_service import MockBookService

script_path = "../"
sys.path.append(script_path)

username = os.environ.get('USER', os.environ.get('USERNAME'))
database_name = "bookshelf_test"
database_path = "postgresql://{}:{}@{}/{}".format(username, username, 'localhost:5432', database_name)


class BaseTestCase(unittest.TestCase):
    """Base class for all test cases."""

    mock_book_service = MockBookService()

    def setUp(self):
        inject.configure(lambda binder: binder
                         .bind(AuthInterface, MockAuth())
                         .bind_to_provider(BookServiceBase, lambda: self.mock_book_service),
                         allow_override=True,
                         clear=True)

        self.database_name = database_name
        self.database_path = database_path
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path
        })

        self.client = self.app.test_client()

        self.with_context(db.create_all)

    def tearDown(self):
        inject.clear()
        self.drop_all()

    def drop_all(self):
        with self.app.app_context():
            db.drop_all()
            db.session.remove()

    def with_context(self, func):
        """
        Runs the given function within the app's context.

        This is useful for running database operations or other app-specific logic
        in test files that inherit from this class.

        :param func: The function to execute within the app context.
        """
        with self.app.app_context():
            func()

    def assert_error(self, res, expect_status_code, expect_message):
        """
        Asserts that the response is an error response with the specified status code and message.
        """
        self.assertEqual(expect_status_code, res.status_code)
        message = res.get_json().get('message')
        self.assertEqual(expect_message, message)

    @staticmethod
    def _get_headers(permissions):
        return {
            "Authorization": f'Bearer {json.dumps({"sub": "auth0|test_user", "permissions": permissions})}'
        }
