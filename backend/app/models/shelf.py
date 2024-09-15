"""
This module defines the database models for shelves and their relationships.

Classes:
- Shelf: Represents a bookshelf, associated with a user, that can contain multiple books.

The models support serialization to/from JSON, making them suitable for use in APIs.
"""
import enum

class ShelfEnum(enum.Enum):
    WANT_TO_READ = 1
    CURRENTLY_READING = 2
    READ = 3

    @classmethod
    def to_str(cls, shelf: 'ShelfEnum') -> str:
        """Maps the enum to JSON/URL path string."""
        mapping = {
            cls.WANT_TO_READ: 'want-to-read',
            cls.CURRENTLY_READING: 'currently-reading',
            cls.READ: 'read'
        }
        return mapping[shelf]

    @classmethod
    def from_str(cls, url: str) -> 'ShelfEnum':
        """Maps a from JSON/URL path string back to the enum."""
        reverse_mapping = {
            'want-to-read': cls.WANT_TO_READ,
            'currently-reading': cls.CURRENTLY_READING,
            'read': cls.READ
        }
        return reverse_mapping[url]