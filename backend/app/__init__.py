"""Flask app for ADB Books API.

This module initializes the Flask app.
It's responsible for setting up the database, configuring CORS, injecting dependencies,
and registers the blueprints for different functionalities.
"""
from flask import (
    Flask,
    jsonify,
)

from app.di.di_config import initialize_di

initialize_di()

from flask_cors import CORS

from .auth.auth import requires_auth, AuthError
from .booklist import booklist_bp
from .di import di_config
from .exceptions.invalid_request_error import InvalidRequestError
from .exceptions.json_error import json_error
from .models.book import Book
from .models.book_dto import setup_db, db
from .ny_times import ny_times_bp
from .search import search_bp
from .curated_picks import curated_picks_bp

from .models.curated_list import CuratedList
from .models.curated_pick import CuratedPick
from .models.user import User
from .models.book_shelf import BookShelf
from .shelf import shelf_bp


# TODO: Handle DELETE requests with 204 status code if successful
def create_app(test_config=None):
    """Create and configure the Flask app."""
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        setup_db(app)
    else:
        config: dict = test_config
        database_path = str(config.get('SQLALCHEMY_DATABASE_URI'))
        setup_db(app, database_path=database_path)

    CORS(app, resources={r"*": {"origins": "*"}})

    app.register_blueprint(search_bp)
    app.register_blueprint(ny_times_bp)
    app.register_blueprint(booklist_bp)
    app.register_blueprint(shelf_bp)
    app.register_blueprint(curated_picks_bp)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route('/')
    def index():
        return 'Healthy'

    @app.errorhandler(400)
    def not_there(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request",
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found",
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return json_error(
            message=f'Unprocessable: {error}',
            code=422
        )

    @app.errorhandler(500)
    def internal_error(_):
        return json_error(message="Internal Server Error", code=500)

    @app.errorhandler(InvalidRequestError)
    def invalid_request_error(error):
        return json_error(error.message, error.code)

    @app.errorhandler(AuthError)
    def auth_error(error):
        return json_error(error.error['description'], error.status_code)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    return app
