from dataclasses import dataclass
from .book_dto import BookDto

def _getFromKeyOrRaise(key: str, d: dict[str, str]) -> str :
    
    value = d.get(key)

    if(isinstance(value, str)):
        if(bool(value.strip()) is False):
            raise Exception('Value of: {} cannot be empty'.format(key))

        return value
    else:
        raise Exception('Missing value for key: {}'.format(key))

def _getOptionalRatingOrRaise(key: str, d: dict[str, str]) -> int :
    
    rating = d.get(key, 0)

    try:
        return int(rating)
    except:
        raise Exception('Value of key rating is not expected type int, value is: {}'.format(rating))
 
@dataclass
class Book():
    id: str
    title: str
    author: str
    rating: int

    def __init__(self, id: str, title: str, author: str, rating: int):
        self.id = id
        self.title = title
        self.author = author
        self.rating = rating

    @classmethod
    def fromDict(cls, d: dict[str, str]):
        return cls(
            id= _getFromKeyOrRaise(key='id', d=d),
            title= _getFromKeyOrRaise(key='title', d=d),
            author= _getFromKeyOrRaise(key='author', d=d),
            rating= _getOptionalRatingOrRaise(key='rating', d=d),
            )

    @classmethod
    def fromDto(cls, dto: BookDto):
        return cls(
            id= dto.bookId,
            title= dto.title,
            author= dto.author,
            rating= dto.rating,
            )