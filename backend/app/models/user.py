"""
This module defines the database models for users and their relationships.

Classes:
- User: Represents a user with a unique ID, username, and email.

The models support serialization to/from JSON, making them suitable for use in APIs.
"""
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.models.book_dto import db
from app.models.book_shelf import BookShelf


class User(db.Model):
    """
    A class that represents a User entity in the database.

    This class is used to store user-specific information, such as username and email,
    and manages the relationship between a user and their associated bookshelves.
    It also supports serialization and deserialization of user data to/from JSON,
    making it suitable for API interactions.
    """
    __tablename__ = 'users'

    userID = Column(String, primary_key=True, unique=True, nullable=False)

    username = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    # Relationship to shelves
    bookshelves = relationship(BookShelf, backref='user', lazy=True)

    def insert(self):
        """
        Inserts the User object into the database.
        """
        db.session.add(self)
        db.session.commit()
