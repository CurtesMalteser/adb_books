# Makes book_managment_api module available,
# if test_book_managment_api.py run from test dir, since the scriptpath is a relative path.
import sys
scriptpath = "../"
sys.path.append(scriptpath)

import os
username = os.environ.get('USER', os.environ.get('USERNAME'))
database_name = "bookshelf_test"
database_path = "postgresql://{}:{}@{}/{}".format(username, username,'localhost:5432', database_name)


import unittest
from book_managment_api import create_app
from book_managment_api.models.book_dto import BookDto, db
from book_managment_api.models.book import Book
import os
import unittest

def withContext(app, func):
    with app.app_context():
        func()

def setUpDb():
    books = [
        BookDto(bookId="1",title="Book 1",author= "Author 1",rating= 1),
        BookDto(bookId="2",title="Book 2",author= "Author 2",rating= 2),
        BookDto(bookId="3",title="Book 3",author= "Author 3",rating= 3),
        BookDto(bookId="4",title="Book 4",author= "Author 4",rating= 4),
        BookDto(bookId="5",title="Book 5",author= "Author 5",rating= 5),
        BookDto(bookId="6",title="Book 6",author= "Author 6",rating= 6),
        BookDto(bookId="7",title="Book 7",author= "Author 7",rating= 7),
        BookDto(bookId="8",title="Book 8",author= "Author 8",rating= 8),
        BookDto(bookId="9",title="Book 9",author= "Author 9",rating= 9),
        BookDto(bookId="10",title="Book 10",author= "Author 10",rating= 10),
        BookDto(bookId="11",title="Book 11",author= "Author 11",rating= 11),
        ]

    db.session.add_all(books)
    db.session.commit()
    db.session.close()

def tearDownDb():
    db.drop_all()
    db.session.close()

class BookManagementApiTestCase(unittest.TestCase):

    def setUp(self):
        self.database_name = database_name
        self.database_path = database_path
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path
        })

        self.client = self.app.test_client

        withContext(self.app, func=setUpDb)


    def tearDown(self):
        withContext(self.app, tearDownDb)
        pass

    def test_get_books_success(self):
        res = self.client().get('/books')

        self.assertEqual(200, res.status_code)

    def test_get_books_pagination(self):
        res = self.client().get('/books?page=2')
        self.assertEqual(200, res.status_code)

    def test_get_books_max_books_size_success(self):
        res = self.client().get('/books?page=1&size=100')
        json = res.get_json()
        books = list(json.get('books'))

        self.assertEqual(10, len(books))

    def test_get_books_non_existing_page_failure_400(self):
        res = self.client().get('/books?page=1000')

        self.assertEqual(400, res.status_code)

    def test_get_books_not_available_db_failure_500(self):
        withContext(self.app, tearDownDb)
        res = self.client().get('/books')

        self.assertEqual(500, res.status_code)

    def test_fake_end_point_expected_404(self):
        res = self.client().get('/fake_end_point')

        self.assertEqual(404, res.status_code)

    def test_delete_book_success(self):
        res = self.client().delete('/book/1')

        self.assertEqual(200, res.status_code)

    def test_delete_non_existing_book_failure_400(self):
        res = self.client().delete('/book/1000')

        self.assertEqual(400, res.status_code)


    def test_add_book_success(self):
        res = self.client().post('/book', data='{"id": "100", "title": "Book 100", "author": "Author 100", "rating": 5}', content_type='application/json')

        self.assertEqual(200, res.status_code)

    def test_add_book_missing_title_failure_422(self):
        res = self.client().post('/book', data='{"id": "100", "author": "Author 100", "rating": 5}', content_type='application/json')

        self.assertEqual(422, res.status_code)

    def test_add_book_missing_rating_success(self):
        res = self.client().post('/book', data='{"id": "100", "title": "Book 100", "author": "Author 100"}', content_type='application/json')

        self.assertEqual(200, res.status_code)

    def test_update_book_rating_success(self):
        book_id = '1'
        book_rating = 5
        res = self.client().patch("/book/{}".format(book_id), data='{{"rating": {}}}'.format(book_rating), content_type='application/json')

        res = self.client().get('/books')
        books = res.get_json().get('books')
        books = map(lambda d : Book.fromDict(d = d), books)
        book = next(filter(lambda b: b.id == book_id, books))

        self.assertEqual(book_rating, book.rating)
        self.assertEqual(200, res.status_code)
        

    def test_update_book_rating_fails_if_rating_not_included(self):
        book_id = '1'
        res = self.client().patch("/book/{}".format(book_id), data='{"id": "100", "author": "Author 100"', content_type='application/json')

        self.assertEqual(400, res.status_code)
        self.assertEqual('Bad request', res.get_json().get('message'))


    def test_search_books_that_matches_query_success(self):
        res = self.client().post('/books', data='{"search": "ok 1"}', content_type='application/json')

        books = res.get_json().get('books')
        books = map(lambda d : Book.fromDict(d = d), books)        

        self.assertEqual(200, res.status_code)
        self.assertEqual(3, len(list(books)))

    def test_search_books_no_matches_query_success(self):
        res = self.client().post('/books', data='{"search": "no books"}', content_type='application/json')

        books = res.get_json().get('books')  

        self.assertEqual(200, res.status_code)
        self.assertEqual(0, len(list(books)))

    def test_search_bad_request_missing_search(self):
        res = self.client().post('/books', content_type='application/json')

        self.assertEqual(400, res.status_code)
        self.assertEqual('Bad request', res.get_json().get('message'))

if __name__ == "__main__":
    unittest.main()