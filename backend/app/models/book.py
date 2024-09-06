"""
Book model
"""
from dataclasses import dataclass


def _get_from_authors_or_raise(key, d: dict[str, str]) -> list[str]:
    """
    :param d: Book JSON dictionary
    :return: list of authors
    :rtype: list[str]
    """
    value = d.get(key)

    if isinstance(value, list):
        return value
    else:
        raise Exception('Missing value for key: {}'.format(key))

def _get_from_key_or_raise(key: str, d: dict[str, str]) -> str :

    value = d.get(key)

    if isinstance(value, str):
        if bool(value.strip()) is False:
            raise Exception('Value of: {} cannot be empty'.format(key))

        return value
    else:
        raise Exception('Missing value for key: {}'.format(key))

def _get_optional_float_or_raise(key: str, d: dict[str, str]) -> float :

    rating = d.get(key, 0)

    try:
        return float(rating)
    except:
        raise Exception('Value of key rating is not expected type number, value is: {}'.format(rating))


@dataclass
class Book:
    """
    A class to represent a book with serialization to/from JSON and DTO.
    """
    id: str
    isbn: str
    isbn13: str
    title: str
    subtitle: str
    authors: list[str]
    image: str
    rating: float
    msrp: float
    language: str
    publisher: str | None
    date_published: str | None
    shelf: str | None
    synopsis: str | None
    pages: int | None
    subjects: list[str]

    def __init__(self,
                 isbn: str,
                 isbn13: str,
                 title: str,
                 subtitle: str,
                 authors: list[str],
                 image: str,
                 rating: float,
                 msrp: float,
                 language: str,
                 publisher: str | None,
                 date_published: str | None,
                 shelf: str | None,
                 synopsis: str | None,
                 pages: int | None,
                 subjects: list[str],
                 ):
        self.id = isbn
        self.isbn = isbn
        self.isbn13 = isbn13
        self.title = title
        self.subtitle = subtitle
        self.authors = authors
        self.image = image
        self.rating = rating
        self.msrp = msrp
        self.language = language
        self.publisher = publisher
        self.date_published = date_published
        self.shelf = shelf
        self.synopsis = synopsis
        self.pages = pages
        self.subjects = subjects

    @classmethod
    def from_json(cls, d: dict[str, str]):
        """
        :param d: Book JSON dictionary
        :return: Book object
        """
        return cls(
            isbn= _get_from_key_or_raise(key='isbn', d=d),
            isbn13= _get_from_key_or_raise(key='isbn13', d=d),
            title= _get_from_key_or_raise(key='title', d=d),
            subtitle= d.get('title_long', ''),
            authors= d.get('authors', []) if d.get('subjects') else None,
            image= _get_from_key_or_raise(key='image', d=d),
            rating= _get_optional_float_or_raise(key='rating', d=d),
            msrp= _get_optional_float_or_raise(key='msrp', d=d),
            language= _get_from_key_or_raise(key='language', d=d),
            publisher= d.get('date_published', None),
            date_published = d.get('date_published', None),
            shelf = d.get('shelf', None),
            synopsis = d.get('synopsis', None),
            pages = d.get('pages', None),
            subjects= d.get('subjects', []) if d.get('subjects') else None,
            )
    # TODO: implement new types on BookDto and migrate table
    # @classmethod
    # def fromDto(cls, dto: BookDto):
    #     return cls(
    #         id= dto.bookId,
    #         title= dto.title,
    #         author= dto.author,
    #         rating= dto.rating,
    #         )