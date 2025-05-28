"""This module contains the CuratedPick model."""
from dataclasses import dataclass

from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    UniqueConstraint, select,
)
from sqlalchemy.orm import relationship

from app.models.book import _get_from_key_or_raise
from app.models.book_dto import db
from app.utils.isbn_utils import is_valid_isbn10, is_valid_isbn13

target_metadata = db.metadata


class CuratedPick(db.Model):
    """
    A class that represents a single book pick within a curated list.

    This class is used to associate a book with a specific position within a curated list.
    """
    __tablename__ = 'curated_picks'

    id = Column(Integer, primary_key=True)
    list_id = Column(Integer, ForeignKey('curated_lists.id', ondelete='CASCADE'), nullable=False)
    isbn13 = Column(String(13), nullable=True)
    isbn10 = Column(String(10), nullable=True)
    position = Column(Integer, nullable=False)

    # Relationship back to CuratedList
    curated_list = relationship('CuratedList', back_populates='curated_picks')

    __table_args__ = (
        UniqueConstraint('list_id', 'position', name='uq_curated_list_position'),
    )

    def __init__(self, list_id, isbn13, isbn10, position):
        """Initialize a CuratedPick instance."""
        self.list_id = list_id
        self.isbn13 = isbn13
        self.isbn10 = isbn10
        self.position = position

    def __str__(self):
        """Provides a string representation of the CuratedPick instance."""
        return f'CuratedPick(list_id={self.list_id}, isbn13={self.isbn13}, isbn10={self.isbn10}, position={self.position})'

    def insert(self):
        """Inserts a new curated pick into the database."""
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Updates the existing curated pick in the database."""
        db.session.commit()

    def delete(self):
        """Deletes the curated pick from the database."""
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_list_id(cls, list_id: int):
        """Retrieves all curated picks associated with a specific list ID."""
        stmt = select(cls).filter_by(list_id=list_id)
        return db.session.execute(stmt).scalars().all()


@dataclass
class CuratedPickRequest:
    """A dataclass that represents a response for a CuratedList object."""
    list_id: int
    position: int
    id: int | None = None
    isbn13: str | None = None
    isbn10: str | None = None

    @classmethod
    def from_model(cls, model: CuratedPick) -> 'CuratedPickRequest':
        """
        Converts a CuratedPick model instance into a CuratedPickRequest dataclass instance.

        :param model: CuratedPick
        :return: CuratedPickRequest instance
        """
        return cls(
            list_id=model.list_id,
            isbn13=model.isbn13,
            isbn10=model.isbn10,
            position=model.position,
        )

    def to_dict(self) -> dict:
        """
        Converts the dataclass instance into a dictionary.

        Add ISBNs dynamically if they are present.
        Client should check for the presence of ISBNs before using them.

        :return: A dictionary with field names as keys and their corresponding field values.
        """
        result = {
            'id': self.id,
            'list_id': self.list_id,
            'position': self.position,
        }

        if self.isbn13:
            result['isbn13'] = self.isbn13
        if self.isbn10:
            result['isbn10'] = self.isbn10

        return result

    @classmethod
    def from_json(cls, d: dict[str, str]) -> 'CuratedPickRequest':
        """
        Create a CuratedPick object from a JSON dictionary.

        :param d: CuratedPick JSON dictionary
        :return: CuratedPick object
        """
        return cls(
            list_id=int(_get_from_key_or_raise(key='list_id', d=d)),
            isbn13=d.get('isbn13', None),
            isbn10=d.get('isbn10', None),
            position=int(_get_from_key_or_raise(key='position', d=d)),
        )

    def __post_init__(self):
        """
        Validate the provided ISBNs to ensure they are in a correct format.

        :raise ValueError: If the ISBNs are not valid.
        """
        if not self.isbn10 and not self.isbn13:
            raise ValueError("At least one of 'isbn10' or 'isbn13' must be provided.")

        if self.isbn10 and not is_valid_isbn10(self.isbn10):
            raise ValueError("Invalid ISBN-10 format.")

        if self.isbn13 and not is_valid_isbn13(self.isbn13):
            raise ValueError("Invalid ISBN-13 format.")
