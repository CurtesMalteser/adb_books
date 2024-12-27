import unittest

from app.models.book import Book
from app.models.book_dto import BookDto, db
from base_test_case import BaseTestCase


def setUpDb():
    books = [
        BookDto(isbn13="1", title="Book 1", authors=["Author 1"], image=None),
        BookDto(isbn13="2", title="Book 2", authors=["Author 2"], image=None),
        BookDto(isbn13="3", title="Book 3", authors=["Author 3"], image=None),
        BookDto(isbn13="4", title="Book 4", authors=["Author 4"], image=None),
        BookDto(isbn13="5", title="Book 5", authors=["Author 5"], image=None),
        BookDto(isbn13="6", title="Book 6", authors=["Author 6"], image=None),
        BookDto(isbn13="7", title="Book 7", authors=["Author 7"], image=None),
        BookDto(isbn13="8", title="Book 8", authors=["Author 8"], image=None),
        BookDto(isbn13="9", title="Book 9", authors=["Author 9"], image=None),
        BookDto(isbn13="10", title="Book 10", authors=["Author 10"], image=None),
        BookDto(isbn13="11", title="Book 11", authors=["Author 11"], image=None),
    ]

    db.session.add_all(books)
    db.session.commit()
    db.session.close()


class BookManagementApiTestCase(BaseTestCase):

    def setUp(self):
        setUpDb()

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
        self.drop_all()
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
        res = self.client().post('/book',
                                 data='{"id": "100", "title": "Book 100", "author": "Author 100", "rating": 5}',
                                 content_type='application/json')

        self.assertEqual(200, res.status_code)

    def test_add_book_missing_title_failure_422(self):
        res = self.client().post('/book', data='{"id": "100", "author": "Author 100", "rating": 5}',
                                 content_type='application/json')

        self.assertEqual(422, res.status_code)

    def test_add_book_missing_rating_success(self):
        res = self.client().post('/book', data='{"id": "100", "title": "Book 100", "author": "Author 100"}',
                                 content_type='application/json')

        self.assertEqual(200, res.status_code)

    def test_update_book_rating_success(self):
        book_id = '1'
        book_rating = 5
        self.client().patch("/book/{}".format(book_id), data='{{"rating": {}}}'.format(book_rating),
                                  content_type='application/json')

        res = self.client().get('/books')
        books = res.get_json().get('books')
        books = map(lambda d: Book.from_json(d=d), books)
        book = next(filter(lambda b: b.id == book_id, books))

        self.assertEqual(book_rating, book.rating)
        self.assertEqual(200, res.status_code)

    def test_update_book_rating_fails_if_rating_not_included(self):
        book_id = '1'
        res = self.client().patch("/book/{}".format(book_id), data='{"id": "100", "author": "Author 100"',
                                  content_type='application/json')

        self.assertEqual(400, res.status_code)
        self.assertEqual('Bad request', res.get_json().get('message'))

    def test_search_books_that_matches_query_success(self):
        res = self.client().post('/books', data='{"search": "curated_picks 1"}', content_type='application/json')

        books = res.get_json().get('books')
        books = map(lambda d: Book.from_json(d=d), books)

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
