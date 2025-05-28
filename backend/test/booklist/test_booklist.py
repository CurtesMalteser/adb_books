import json

from app.models.book_dto import BookDto
from app.models.book_shelf import BookShelf
from app.models.shelf import ShelfEnum
from app.models.user import User
from test.base_test_case import BaseTestCase
from test.utils.isbn_utils import generate_random_isbn13


class BookListTestCase(BaseTestCase):

    @staticmethod
    def _get_user(headers):
        token = headers['Authorization'].split(' ', 1)[1]
        token_dict = json.loads(token)
        return token_dict.get('sub')

    @staticmethod
    def _setup_bookshelf(user: str, shelf: ShelfEnum):
        User(userID=user, username='test', email='').insert()
        for i in range(1, 8):  # 7 books
            isbn13 = generate_random_isbn13()
            BookDto(
                title=f'Mock Book {i}',
                authors=[f'Mock Author {i}'],
                image='',
                isbn13=isbn13).insert()
            BookShelf(isbn13=isbn13, user_id=user, shelf=shelf).insert()

    def test_get_booklist_returns_200_empty_list(self):
        res = self.client.get('/booklist/read', headers=self._get_headers(["booklist:get"]))

        self.assertEqual(200, res.status_code)
        self.assertEqual([], res.json['books'])

    def test_get_booklist_returns_404_invalid_shelf(self):
        res = self.client.get('/booklist/test', headers=self._get_headers(["booklist:get"]))

        self.assert_error(res, expect_status_code=404, expect_message="Shelf: 'test' not found.")

    def test_get_booklist_returns_200_booklist_with_pagination(self):
        headers = self._get_headers(["booklist:get"])
        self.with_context(
            lambda: self._setup_bookshelf(self._get_user(headers), ShelfEnum.READ)
        )
        res = self.client.get('/booklist/read?page=2&limit=3', headers=headers)

        self.assertEqual(200, res.status_code)
        self.assertEqual(3, len(res.json['books']))
        self.assertEqual(2, res.json['page'])
        self.assertEqual(3, res.json['limit'])
        self.assertEqual(7, res.json['total_results'])

    def test_get_booklist_returns_403_permission_not_found(self):
        res = self.client.get('/booklist/test', headers=self._get_headers(["test:get"]))

        self.assert_error(res, expect_status_code=403, expect_message='Permission not found.')
