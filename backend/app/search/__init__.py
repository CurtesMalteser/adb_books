import os
from flask import Blueprint
from flask_cors import cross_origin
from app.search.books import books
from app.search.shelves import shelves

base_url = os.environ.get('BASE_URL')
user_agent = os.environ.get('USER_AGENT')

search_bp = Blueprint('search', __name__)

@search_bp.route('/search/books')
@cross_origin()
def search_books():
    return books(base_url=base_url, user_agent=user_agent)

@search_bp.route('/search/shelves')
@cross_origin()
def search_shelves():
    return shelves()