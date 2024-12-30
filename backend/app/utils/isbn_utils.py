"""
ISBN-10 and ISBN-13 validation utilities.
"""
import re


def is_valid_isbn10(isbn: str) -> bool:
    """
    Validate ISBN-10.
    :param isbn: ISBN-10 string
    :return: True if valid, False otherwise
    """
    if len(isbn) != 10:
        return False

    if not re.match(r'^\d{9}[\dX]$', isbn):
        return False

    total = sum((i + 1) * (10 if char == 'X' else int(char)) for i, char in enumerate(isbn))
    return total % 11 == 0


def is_valid_isbn13(isbn: str) -> bool:
    """
    Validate ISBN-13.
    :param isbn: ISBN-13 string
    :return: True if valid, False otherwise
    """
    if len(isbn) != 13 or not isbn.isdigit():
        return False

    total = sum((1 if i % 2 == 0 else 3) * int(char) for i, char in enumerate(isbn))
    return total % 10 == 0
