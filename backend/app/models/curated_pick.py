"""
This module contains the CuratedPick model.
"""
from dataclasses import dataclass

from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.models.book import _get_from_key_or_raise
from app.models.book_dto import db
from app.utils.isbn_utils import is_valid_isbn_10, is_valid_isbn_13

target_metadata = db.metadata


class CuratedPick(db.Model):
    """
    A class that represents a single book pick within a curated list.
    This class is used to associate a book with a specific position within a curated list.
    """
    __tablename__ = 'curated_picks'

    id = Column(Integer, primary_key=True)
    list_id = Column(Integer, ForeignKey('curated_lists.id', ondelete='CASCADE'), nullable=False)
    isbn_13 = Column(String(13), nullable=True)
    isbn_10 = Column(String(10), nullable=True)
    position = Column(Integer, nullable=False)

    # Relationship back to CuratedList
    curated_list = relationship('CuratedList', back_populates='curated_picks')

    __table_args__ = (
        UniqueConstraint('list_id', 'position', name='uq_curated_list_position'),
    )

    def __init__(self, list_id, isbn_13, isbn_10, position):
        self.list_id = list_id
        self.isbn_13 = isbn_13
        self.isbn_10 = isbn_10
        self.position = position

    def __str__(self):
        return f'CuratedPick(list_id={self.list_id}, isbn_13={self.isbn_13}, isbn_10={self.isbn_10}, position={self.position})'

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


@dataclass
class CuratedPickRequest:
    """
    A dataclass that represents a response for a CuratedList object.
    """
    list_id: int
    position: int
    id: int | None = None
    isbn_13: str | None = None
    isbn_10: str | None = None

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

        if self.isbn_13:
            result['isbn_13'] = self.isbn_13
        if self.isbn_10:
            result['isbn_10'] = self.isbn_10

        return result

    @classmethod
    def from_json(cls, d: dict[str, str]) -> 'CuratedPickRequest':
        """
        :param d: CuratedPick JSON dictionary
        :return: CuratedPick object
        """
        return cls(
            list_id=int(_get_from_key_or_raise(key='list_id', d=d)),
            isbn_13=d.get('isbn_13', None),
            isbn_10=d.get('isbn_10', None),
            position=int(_get_from_key_or_raise(key='position', d=d)),
        )

    def __post_init__(self):
        if not self.isbn_10 and not self.isbn_13:
            raise ValueError("At least one of 'isbn_10' or 'isbn_13' must be provided.")

        if self.isbn_10 and not is_valid_isbn_10(self.isbn_10):
            raise ValueError("Invalid ISBN-10 format.")

        if self.isbn_13 and not is_valid_isbn_13(self.isbn_13):
            raise ValueError("Invalid ISBN-13 format.")
