"""This module provides routes to fetch best-selling books from The New York Times API."""
from flask import Blueprint
from flask_cors import cross_origin

from app.auth.auth import requires_auth
from app.config import (
    FICTION_PATH,
    NON_FICTION_PATH,
)
from app.ny_times.books import fetch_books

ny_times_bp = Blueprint('ny-times', __name__)


@ny_times_bp.route('/ny-times/best-sellers/fiction')
@cross_origin()
@requires_auth('booklist:get')
def fetch_fiction(_):
    """
    Data provided by The New York Times.

    For details visit: https://developer.nytimes.com.
    Fetches "Combined Print and E-Book Fiction" list.
    :return: JSON array of books if the request is successful, or aborts with an error response.
    :rtype: list or flask.Response
    """
    return fetch_books(path=FICTION_PATH)


@ny_times_bp.route('/ny-times/best-sellers/non-fiction')
@cross_origin()
@requires_auth('booklist:get')
def fetch_non_fiction(_):
    """
    Data provided by The New York Times.

    For details visit: https://developer.nytimes.com.
    Fetches "Combined Print & E-Book Nonfiction" list.
    :return: JSON array of books if the request is successful, or aborts with an error response.
    :rtype: list or flask.Response
    """
    return fetch_books(path=NON_FICTION_PATH)
