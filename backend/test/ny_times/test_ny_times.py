import unittest

from app.config import FICTION_PATH, NON_FICTION_PATH
from test.base_test_case import BaseTestCase


class NyTimesTestCase(BaseTestCase):

    @staticmethod
    def _mock_books():
        return [
            {
                "authors": [
                    "Author 1"
                ],
                "image": "book1.jpg",
                "isbn10": "isbn10",
                "isbn13": "9780000000001",
                "title": "Book 1"
            },
            {
                "authors": [
                    "Author 2"
                ],
                "image": "book2.jpg",
                "isbn10": "isbn10",
                "isbn13": "9780000000002",
                "title": "Book 2"
            },
            {
                "authors": [
                    "Book 3"
                ],
                "image": "book3.jpg",
                "isbn10": "isbn10",
                "isbn13": "9780000000003",
                "title": "Book 3"
            }
        ]

    def test_fetch_fiction_403_permission_not_found(self):
        res = self.client.get('/ny-times/best-sellers/fiction', headers=self._get_headers(["test:get"]))
        self.assert_error(res, expect_status_code=403, expect_message='Permission not found.')

    def test_fetch_fiction_200_return_empty_list(self):
        self.mock_nyt_service.mock_books(path=FICTION_PATH, books=[])
        res = self.client.get('/ny-times/best-sellers/fiction', headers=self._get_headers(["booklist:get"]))
        self.assertEqual(200, res.status_code)
        self.assertEqual(0, len(res.json['books']))

    def test_fetch_fiction_with_permission_500_internal_server_error(self):
        self.mock_nyt_service.mock_books(path=FICTION_PATH, books=[])
        self.mock_nyt_service.mock_error(True)
        res = self.client.get('/ny-times/best-sellers/fiction', headers=self._get_headers(["booklist:get"]))
        self.assert_error(res, expect_status_code=500, expect_message='Internal Server Error')

    def test_fetch_non_fiction_403_permission_not_found(self):
        res = self.client.get('/ny-times/best-sellers/non-fiction', headers=self._get_headers(["test:get"]))
        self.assert_error(res, expect_status_code=403, expect_message='Permission not found.')

    def test_fetch_non_fiction_200_return_empty_list(self):
        self.mock_nyt_service.mock_books(path=NON_FICTION_PATH, books=self._mock_books())
        res = self.client.get('/ny-times/best-sellers/non-fiction', headers=self._get_headers(["booklist:get"]))
        self.assertEqual(200, res.status_code)
        self.assertEqual(3, len(res.json['books']))

    def test_fetch_non_fiction_with_permission_500_internal_server_error(self):
        self.mock_nyt_service.mock_books(path=NON_FICTION_PATH, books=[])
        self.mock_nyt_service.mock_error(True)
        res = self.client.get('/ny-times/best-sellers/non-fiction', headers=self._get_headers(["booklist:get"]))
        self.assert_error(res, expect_status_code=500, expect_message='Internal Server Error')


if __name__ == '__main__':
    unittest.main()
