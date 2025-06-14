"""This module contains the BookDto class and the BookResponse dataclass."""
from dataclasses import dataclass
from os import environ as env
from typing import List, Optional

from dotenv import load_dotenv, find_dotenv
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (Column,
                        String,
                        Integer,
                        ARRAY,
                        select,
                        )
from sqlalchemy.orm import mapped_column

from app.models.book import _get_from_key_or_raise
from app.utils.isbn_utils import is_valid_isbn

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

username = env.get('USER') or env.get('USERNAME')
db_path = env.get('DB_PATH')
db_path = db_path.replace('USER', username)

db = SQLAlchemy()
migrate = Migrate()


def setup_db(app, database_path=db_path):
    """
    Sets up the database connection for the Flask application.

    setup_db(app)
        binds a flask application and a SQLAlchemy service
    """
    with app.app_context():
        app.config["SQLALCHEMY_DATABASE_URI"] = database_path
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.init_app(app)
        migrate.init_app(app, db=db)


class BookDto(db.Model):
    """BookDto model."""
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    isbn13 = mapped_column(String, nullable=False, unique=True)
    title = mapped_column(String, nullable=False)
    authors = Column(ARRAY(String), nullable=False)
    image = db.Column(String, nullable=True, default=None)

    def __init__(self, isbn13, title, authors, image):
        """Initialize a BookDto instance."""
        self.isbn13 = isbn13
        self.title = title
        self.authors = authors
        self.image = image

    def insert(self):
        """Inserts a new book into the database."""
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Updates an existing book in the database."""
        db.session.commit()

    def delete(self):
        """Deletes a book from the database."""
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def search_by_title(cls, title_query: str):
        """Searches for books by title."""
        stmt = select(cls).filter(cls.title.ilike(f"%{title_query}%")).order_by(cls.id)
        return db.session.execute(stmt).scalars().all()


@dataclass
class BookResponse:
    """A class to represent a book with serialization to/from JSON and DTO."""
    isbn13: Optional[str]
    isbn10: Optional[str]
    title: str
    authors: List[str]
    image: str
    shelf: Optional[str]

    def to_dict(self) -> dict:
        """
        Converts the dataclass instance into a dictionary.

        :return: A dictionary with field names as keys and their corresponding field values.
        """
        return {key: value for key, value in self.__dict__.items() if value is not None}

    @classmethod
    def from_json(cls, d: dict[str, str]) -> 'BookResponse':
        """
        Create a Book object from a JSON dictionary.

        :param d: Book JSON dictionary
        :return: Book object
        """
        isbn10 = d.get('isbn10')
        isbn13 = d.get('isbn13')
        is_isbn = is_valid_isbn(isbn10, isbn13)
        if not is_isbn:
            raise ValueError('No ISBN found in JSON.')

        return cls(
            isbn13=d.get('isbn13'),
            isbn10=d.get('isbn10'),
            title=_get_from_key_or_raise(key='title', d=d),
            authors=d.get('authors', []) if d.get('authors') else None,
            image=_get_from_key_or_raise(key='image', d=d),
            shelf=d.get('shelf', None),
        )

    @classmethod
    def from_ny_times_json(cls, d: dict[str, str]) -> 'BookResponse':
        """
        Create a Book object from NYT JSON dictionary.

        :param d: Book JSON dictionary
        :return: Book object
        """
        isbn10 = d.get('primary_isbn10')
        isbn13 = d.get('primary_isbn13')

        is_isbn = is_valid_isbn(isbn10, isbn13)
        if not is_isbn:
            raise ValueError('No ISBN found in NYT JSON.')

        return cls(
            isbn13=isbn13,
            isbn10=isbn10,
            title=_get_from_key_or_raise(key='title', d=d),
            authors=[d.get('author')],
            image=_get_from_key_or_raise(key='book_image', d=d),
            shelf=None,
        )
