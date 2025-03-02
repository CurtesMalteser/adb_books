"""
This module defines the database models for bookshelves and their relationships.

Classes:
- BookShelf: Serves as an association table to implement the many-to-many relationship between books and shelves.

The models support serialization to/from JSON, making them suitable for use in APIs.
"""
from sqlalchemy import (Column,
                        String,
                        ForeignKey,
                        Enum,
                        UniqueConstraint,
                        Integer, event,
                        )

from app.models.book_dto import db, BookDto
from app.models.shelf import ShelfEnum


class BookShelf(db.Model):
    """
    A class that represents the association between books and shelves in a many-to-many relationship.

    This class is used to link books (identified by ISBN13) with shelves. Each record associates
    a specific book with a specific shelf for a user, and it also helps to serialize and deserialize
    data to/from JSON for easy API integration.
    """
    __tablename__ = 'book_shelves'

    id = Column(Integer, primary_key=True, autoincrement=True)
    isbn13 = Column(String, ForeignKey('books.isbn13'), nullable=False)
    userID = Column(String, ForeignKey('users.userID'), nullable=False)
    shelf = Column(Enum(ShelfEnum), nullable=False)

    __table_args__ = (UniqueConstraint('isbn13', 'userID', name='_isbn13_user_uc'),)

    def __init__(self, isbn13, user_id, shelf):
        self.isbn13 = isbn13
        self.userID = user_id
        self.shelf = shelf

    def insert(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_or_none(book_id, user_id) -> 'BookShelf':
        return BookShelf.query.filter_by(
            isbn13=book_id,
            userID=user_id
        ).one_or_none()


def _delete_book_if_orphaned(isbn13):
    # Check if any BookShelf entries are left for this ISBN
    remaining_shelves = BookShelf.query.filter_by(isbn13=isbn13).count()
    if remaining_shelves == 0:
        # If no shelves are left for the book, delete the book
        book = BookDto.query.filter_by(isbn13=isbn13).one_or_none()
        if book:
            book.delete()

@event.listens_for(db.session, 'after_flush')
def check_for_orphaned_books(session, _):
    # Call your orphan check logic here
    for obj in session.deleted:
        if isinstance(obj, BookShelf):
            _delete_book_if_orphaned(obj.isbn13)