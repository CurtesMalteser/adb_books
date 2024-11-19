"""
This module contains the CuratedPick model.
"""
from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from app.models.book_dto import db

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
