"""
Utility functions for generating mock ISBN13s.
"""
import random


def generate_random_isbn13() -> str:
    """
    Generate a valid random ISBN-13.
    :return: A valid random ISBN-13.
    """
    prefix = '978'  # Common prefix for ISBN-13
    body = ''.join(str(random.randint(0, 9)) for _ in range(9))
    partial_isbn = prefix + body

    # Calculate the check digit
    total = sum((3 if i % 2 else 1) * int(digit) for i, digit in enumerate(partial_isbn))
    check_digit = (10 - (total % 10)) % 10

    return partial_isbn + str(check_digit)
