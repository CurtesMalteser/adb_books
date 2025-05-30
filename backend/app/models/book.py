"""Book model."""
from dataclasses import dataclass
from typing import List, Optional


def _get_from_authors_or_raise(key, d: dict[str, str]) -> list[str]:
    """
    Get authors from the JSON dictionary.

    :param d: Book JSON dictionary
    :return: list of authors
    :rtype: list[str]
    """
    value = d.get(key)

    if isinstance(value, list):
        return value
    else:
        raise Exception('Missing value for key: {}'.format(key))


def _get_from_key_or_raise(key: str, d: dict[str, str]) -> str:
    value = d.get(key)

    if isinstance(value, str):
        if bool(value.strip()) is False:
            raise Exception('Value of: {} cannot be empty'.format(key))

        return value
    else:
        raise Exception('Missing value for key: {}'.format(key))


def _get_optional_float_or_raise(key: str, d: dict[str, str]) -> float:
    rating = d.get(key, 0)

    try:
        return float(rating)
    except Exception as e:
        print(f'🧨 {e}')
        raise Exception('Value of key rating is not expected type number, value is: {}'.format(rating))


@dataclass
class Book:
    """A class to represent a book with serialization to/from JSON and DTO."""
    isbn: Optional[str]
    isbn13: str
    title: str
    subtitle: str
    authors: List[str]
    image: str
    rating: float
    msrp: float
    language: str
    publisher: Optional[str]
    date_published: Optional[str]
    shelf: Optional[str]
    synopsis: Optional[str]
    pages: Optional[int]
    subjects: List[str]

    def to_dict(self) -> dict:
        """
        Converts the dataclass instance into a dictionary.

        :return: A dictionary with field names as keys and their corresponding field values.
        """
        return {key: value for key, value in self.__dict__.items() if value is not None}

    @classmethod
    def from_json(cls, d: dict[str, str]):
        """
        Create a Book object from a JSON dictionary.

        :param d: Book JSON dictionary
        :return: Book object
        """
        return cls(
            isbn=_get_from_key_or_raise(key='isbn', d=d),
            isbn13=_get_from_key_or_raise(key='isbn13', d=d),
            title=_get_from_key_or_raise(key='title', d=d),
            subtitle=d.get('title_long', ''),
            authors=d.get('authors', []) if d.get('authors') else None,
            image=_get_from_key_or_raise(key='image', d=d),
            rating=_get_optional_float_or_raise(key='rating', d=d),
            msrp=_get_optional_float_or_raise(key='msrp', d=d),
            language=_get_from_key_or_raise(key='language', d=d),
            publisher=d.get('date_published', None),
            date_published=d.get('date_published', None),
            shelf=d.get('shelf', None),
            synopsis=d.get('synopsis', None),
            pages=d.get('pages', None),
            subjects=d.get('subjects', []) if d.get('subjects') else None,
        )
