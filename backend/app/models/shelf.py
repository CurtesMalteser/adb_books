"""
This module defines the database models for shelves and their relationships.

Classes:
- Shelf: Represents a bookshelf, associated with a user, that can contain multiple books.

The models support serialization to/from JSON, making them suitable for use in APIs.
"""
from sqlalchemy import (Column,
                        String,
                        Integer,
                        ForeignKey,
                        )
from sqlalchemy.orm import relationship

from app.models.book_dto import db
from app.models.book_shelf import BookShelf


class Shelf(db.Model):
    """
    A class that represents a Shelf entity in the database.

    This class is used to store information about a user's bookshelf, including the shelf's name and
    its association with a specific user. It is also used to manage relationships between shelves
    and the books they contain, as well as to serialize and deserialize the data to/from JSON for
    API interactions.
    """
    __tablename__ = 'shelves'

    shelfID = Column(Integer, primary_key=True)
    shelf_name = Column(String(50), nullable=False)
    userID = Column(String, ForeignKey('users.userID'), nullable=False)

    books = relationship(BookShelf, backref='shelf', lazy=True)