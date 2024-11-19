"""
This module contains the CuratedList model.
"""
from sqlalchemy import (
    Column,
    String,
    Integer,
    Text,
)
from sqlalchemy.orm import relationship
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
