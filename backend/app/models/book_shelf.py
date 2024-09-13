"""
This module defines the database models for bookshelves and their relationships.

Classes:
- BookShelf: Serves as an association table to implement the many-to-many relationship between books and shelves.

The models support serialization to/from JSON, making them suitable for use in APIs.
"""
from sqlalchemy import (Column,
                        String,
                        Integer,
                        ForeignKey,
                        )

from app.models.book_dto import db


class BookShelf(db.Model):
    """
    A class that represents the association between books and shelves in a many-to-many relationship.

    This class is used to link books (identified by ISBN13) with shelves. Each record associates
    a specific book with a specific shelf for a user, and it also helps to serialize and deserialize
    data to/from JSON for easy API integration.
    """
    __tablename__ = 'book_shelves'

    isbn13 = Column(String, ForeignKey('books.isbn13'), primary_key=True)
    userID = Column(String, ForeignKey('users.userID'), primary_key=True)
    shelfID = Column(Integer, ForeignKey('shelves.shelfID'), primary_key=True)
