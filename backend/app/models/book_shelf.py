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
                        Integer, event, select,
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
        """Initialize a BookShelf instance."""
        self.isbn13 = isbn13
        self.userID = user_id
        self.shelf = shelf

    def insert(self):
        """Inserts a new bookshelf association into the database."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Deletes a bookshelf association from the database."""
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_or_none(book_id, user_id) -> 'BookShelf':
        """Retrieves a BookShelf instance by ISBN13 and userID."""
        statement = select(BookShelf).filter_by(
            isbn13=book_id,
            userID=user_id
        )
        result = db.session.execute(statement).scalar_one_or_none()
        return result


def _delete_book_if_orphaned(isbn13):
    # Check if any BookShelf entries are left for this ISBN
    remaining_shelf = db.session.execute(
        select(BookShelf).filter_by(isbn13=isbn13)
    ).scalar_one_or_none()

    if not remaining_shelf:
        book = db.session.execute(
            select(BookDto).filter_by(isbn13=isbn13)
        ).scalar_one_or_none()
        if book:
            db.session.delete(book)


@event.listens_for(db.session, 'after_commit')
def cleanup_orphaned_books(session):
    """
    Cleanup orphaned books after a commit.

    :param session: db.session
    """
    orphaned = session.info.pop('orphaned_books', set())
    for isbn13 in orphaned:
        _delete_book_if_orphaned(isbn13)
