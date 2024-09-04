import json
from flask import (
    Flask,
    jsonify,
    abort,
    request,
    )
from flask_cors import (
    CORS,
    cross_origin,
    )
from .exceptions.invalid_request_error import InvalidRequestError
from .exceptions.json_error import json_error
from .models.book import Book
from .models.book_dto import *
from .pagination.books import paginate
from .search import search_bp


is_success : bool = True

def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        setup_db(app)
    else:
        config: dict = test_config
        database_path = str(config.get('SQLALCHEMY_DATABASE_URI'))
        setup_db(app, database_path=database_path)

    CORS(app, resources={r"*": {"origins": "*"}})

    app.register_blueprint(search_bp)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route('/')
    def index():
        return 'Healthy'

    @app.route('/books')
    @cross_origin()
    def get_books():
        if(is_success):
            def query():
                return BookDto.query.order_by(BookDto.id).all()

            books = paginate(request=request, query=query)

            if books is None:
                abort(400)
            else:
                return books

        else:
            abort(404)

    @app.route('/book', methods=['POST'])
    @cross_origin()
    def add_book():
        if is_success:
            if request.is_json:
                try:
                    json_data = json.dumps(request.json)
                    book = json.loads(json_data, object_hook = lambda d : Book.fromDict(d = d))

                
                    BookDto(bookId = book.id, title=book.title, author= book.author, rating= book.rating).insert()
                
                    return jsonify({
                        "success": True,
                        "book": book
                    })

                except:
                    db.session.rollback()
                    abort(422)
                finally:
                    db.session.close()

            else:
                abort(404, "Content type is not supported.")
        else:
            abort(404, "Mocked failure! Call GET /success.")

    @app.route('/book/<string:book_id>')
    @cross_origin()
    def get_book(book_id: str):
        error = False
        book = None
        try:
            book_dto = BookDto.query.filter(BookDto.bookId == str(book_id)).one_or_none()
            if isinstance(book_dto, BookDto):
                # Ignore type cast because it checks if it is a BookDto
                book = Book.fromDto(book_dto) # type: ignore
            else:
                error = True

        except Exception as ex:
            db.session.rollback()
            error = True
            print(f"🧨 error: {ex}")
        finally:
            db.session.close()

        if error:
            abort(400)
        else:
            return jsonify({
                "success": True,
                "book": book,
            })


    @app.route('/book/<string:bookId>', methods=['DELETE'])
    @cross_origin()
    def delete_book(bookId: str):
        if(is_success):
            error = False

            try:
                book = BookDto.query.filter(BookDto.bookId == bookId).one_or_none()
                if book is None:
                    error = True
                else:
                    book.delete()
                    
            except:
                error = True
                db.session.rollback()
            finally:
                db.session.close()

            if(error):
                abort(400)
            else:
               return jsonify({
                            "sucess": True,
                            "deleted": bookId,
                        })
        else:
            abort(404, "Mocked failure! Call GET /success.")

    @app.route('/book/<string:book_id>', methods=['PATCH'])
    @cross_origin()
    def update_book_rating(book_id: str):
        if(is_success):
            if (request.is_json):
                body = request.get_json()
                try:
                    book = BookDto.query.filter(BookDto.id == book_id).one_or_none()

                    if(book is None):
                        abort(404)

                    if('rating' in body):
                        book.rating = int(body.get("rating"))

                    book.update()

                    return jsonify({
                        "sucess": True,
                        "updated": book_id,
                        })

                except:
                    abort(400) 
                        
            else:
                abort(404)
        else:
            abort(404, "Mocked failure! Call GET /success.")

    @app.route('/success')
    @cross_origin()
    def is_success():
        global is_success
        is_success = True
        return jsonify("isSuccess: True")

    @app.route('/failure')
    @cross_origin()
    def is_failure():
        global is_success
        is_success = False
        return jsonify("isSuccess: False")


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
    def internal_error(error):
        return json_error(message="Internal Server Error", code=500)

    @app.errorhandler(InvalidRequestError)
    def invalid_request_error(error):
        return json_error(error.message, error.code)


    return app