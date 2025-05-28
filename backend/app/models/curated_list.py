"""This module contains the CuratedList model."""
from dataclasses import dataclass

from sqlalchemy import (
    Column,
    String,
    Integer,
    Text,
)
from sqlalchemy.orm import relationship

from app.models.book import _get_from_key_or_raise
from app.models.book_dto import db

target_metadata = db.metadata


class CuratedList(db.Model):
    """
    A class that represents a curated list of books.

    This list can be used to group books together based on a specific choice.
    """
    __tablename__ = 'curated_lists'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    # Relationship to CuratedPick
    curated_picks = relationship('CuratedPick', back_populates='curated_list', cascade='all, delete-orphan')

    def __init__(self, name, description):
        """Initialize a CuratedList instance."""
        self.name = name
        self.description = description

    def insert(self):
        """Inserts a new curated list into the database."""
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Updates the existing curated list in the database."""
        db.session.commit()

    def delete(self):
        """Deletes the curated list from the database."""
        db.session.delete(self)
        db.session.commit()


@dataclass
class CuratedListRequest:
    """A dataclass that represents a response for a CuratedList object."""
    name: str
    description: str
    id: int | None = None

    @classmethod
    def from_model(cls, model: CuratedList) -> 'CuratedListRequest':
        """
        Converts a CuratedList model instance into a CuratedListRequest dataclass instance.

        :param model: CuratedList
        :return: CuratedListRequest instance
        """
        return cls(
            name=model.name,
            description=model.description,
            id=model.id if model.id is not None else None,
        )

    def to_dict(self) -> dict:
        """
        Converts the dataclass instance into a dictionary.

        :return: A dictionary with field names as keys and their corresponding field values.
        """
        return {key: value for key, value in self.__dict__.items() if value is not None}

    @classmethod
    def from_json(cls, d: dict[str, str]) -> 'CuratedListRequest':
        """
        Create a CuratedList object from a JSON dictionary.

        :param d: CuratedList JSON dictionary
        :return: CuratedList object
        """
        return cls(
            name=_get_from_key_or_raise(key='name', d=d),
            description=d.get("description", "").strip(),
            id=d.get("id", None),
        )
