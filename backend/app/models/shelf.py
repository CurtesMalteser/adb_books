"""
This module defines the database models for shelves and their relationships.

Classes:
- Shelf: Represents a bookshelf, associated with a user, that can contain multiple books.

The models support serialization to/from JSON, making them suitable for use in APIs.
"""
import enum

class ShelfEnum(enum.Enum):
    NONE = 1
    WANT_TO_READ = 2
    CURRENTLY_READING = 3
    READ = 4

