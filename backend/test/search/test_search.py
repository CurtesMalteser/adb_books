from app.models.book_dto import BookResponse, BookDto
from test.base_test_case import BaseTestCase


class SearchTestCase(BaseTestCase):

    def test_search_books_success(self):
        mock_book = BookResponse(
            isbn13="9781234567897",
            isbn10=None,
            title="Mocked Book",
            authors=["Mocked Author"],
            image="mocked_image.jpg",
            shelf=None
        )

        self.mock_book_service.mock_books([mock_book])

        res = self.client.get(
            '/search/books?q=Mocked',
            headers=self._get_headers(["booklist:get"])
        )

        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(len(data['books']), 1)
        self.assertEqual(data['books'][0]['title'], "Mocked Book")

    def test_search_books_403_for_missing_permission(self):
        res = self.client.get(
            '/search/books?q=test',
            headers=self._get_headers([])  # Empty permissions!
        )

        self.assert_error(res, expect_status_code=403, expect_message='Permission not found.')

    def test_search_books_400_missing_query(self):
        res = self.client.get(
            '/search/books',
            headers=self._get_headers(["booklist:get"])
        )

        self.assertEqual(res.status_code, 400)

    def test_search_shelves_success(self):
        def add_test_book():
            """Add a test book to the database."""
            book = BookDto(
                isbn13="9781234567897",
                title="Test Shelf Book",
                authors=["Test Author"],
                image="test_image.jpg"
            )
            book.insert()

        self.with_context(add_test_book)

        res = self.client.get(
            '/search/shelves?q=Test',
            headers=self._get_headers(["booklist:get"])
        )

        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.get_json()['success'])
        self.assertEqual(len(res.get_json()['books']), 1)

    def test_search_shelves_403_for_missing_permission(self):
        res = self.client.get(
            '/search/shelves?q=Test',
            headers=self._get_headers([])  # Empty permissions
        )

        self.assert_error(res, expect_status_code=403, expect_message='Permission not found.')

    def test_search_shelves_400_missing_query(self):
        res = self.client.get(
            '/search/shelves',
            headers=self._get_headers(["booklist:get"])
        )

        self.assertEqual(res.status_code, 400)
