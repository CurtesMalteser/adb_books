# Makes book_managment_api module available,
# if test_book_managment_api.py run from test dir, since the scriptpath is a relative path.
import os
import sys
import unittest

import inject

from app import create_app
from app.auth.auth_interface import AuthInterface
from app.models.book_dto import db
from test.auth.mock_auth import MockAuth

script_path = "../"
sys.path.append(script_path)

username = os.environ.get('USER', os.environ.get('USERNAME'))
database_name = "bookshelf_test"
database_path = "postgresql://{}:{}@{}/{}".format(username, username, 'localhost:5432', database_name)


class BaseTestCase(unittest.TestCase):
    """Base class for all test cases."""

    def setUp(self):
        inject.configure(lambda binder: binder
                         .bind(AuthInterface, MockAuth()),
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
