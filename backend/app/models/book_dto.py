import os
from dataclasses import dataclass, asdict
from typing import List, Optional

from flask_migrate import Migrate
from sqlalchemy import (Column,
                        String,
                        Integer,
                        ARRAY,
                        )
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import mapped_column

from app.models.book import _get_from_key_or_raise

username = os.environ.get('USER') or os.environ.get('USERNAME')
db_path = os.environ.get('DB_PATH')
db_path = db_path.replace('USER', username)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=db_path):
    with app.app_context():
        app.config["SQLALCHEMY_DATABASE_URI"] = database_path
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.init_app(app)

        migrate = Migrate(app, db)

        with app.app_context():
            db.create_all()


'''
BookDto
'''


class BookDto(db.Model):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    isbn13 = mapped_column(String, nullable=False, unique=True)
    title = mapped_column(String, nullable=False)
    authors = Column(ARRAY(String), nullable=False)
    image = db.Column(String, nullable=True, default=None)
    shelf = db.Column(String, nullable=True, default=None)

    def __init__(self, isbn13, title, author, image, shelf):
        self.isbn13 = isbn13
        self.title = title
        self.author = author
        self.image = image
        self.shelf = shelf

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


@dataclass
class BookResponse:
    """
    A class to represent a book with serialization to/from JSON and DTO.
    """
    isbn13: str
    title: str
    authors: List[str]
    image: str
    shelf: Optional[str]

    def to_dict(self):
        """
        Converts the dataclass instance into a dictionary.

        :return: A dictionary with field names as keys and their corresponding field values.
        """
        return asdict(self)

    @classmethod
    def from_json(cls, d: dict[str, str]):
        """
        :param d: Book JSON dictionary
        :return: Book object
        """
        return cls(
            isbn13=_get_from_key_or_raise(key='isbn13', d=d),
            title=_get_from_key_or_raise(key='title', d=d),
            authors=d.get('authors', []) if d.get('authors') else None,
            image=_get_from_key_or_raise(key='image', d=d),
            shelf=d.get('shelf', None),
        )

    @classmethod
    def from_ny_times_json(cls, d: dict[str, str]):
        """
        :param d: Book JSON dictionary
        :return: Book object
        """
        return cls(
            isbn13=_get_from_key_or_raise(key='primary_isbn13', d=d),
            title=_get_from_key_or_raise(key='title', d=d),
            authors=[d.get('author')],
            image=_get_from_key_or_raise(key='book_image', d=d),
            shelf=None,
        )
