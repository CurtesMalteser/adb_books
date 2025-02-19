import os
from flask import Blueprint
from flask_cors import cross_origin

from app.auth.auth import requires_auth
from app.search.books import books
from app.search.shelves import shelves

user_agent = os.environ.get('USER_AGENT')

search_bp = Blueprint('search', __name__)

@search_bp.route('/search/books')
@cross_origin()
@requires_auth('booklist:get')
def search_books(_):
    return books(user_agent=user_agent)

@search_bp.route('/search/shelves')
@cross_origin()
@requires_auth('booklist:get')
def search_shelves(_):
    return shelves()
