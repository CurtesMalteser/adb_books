import unittest

from app.models.book_dto import BookResponse
from test.base_test_case import BaseTestCase


class ShelfTestCase(BaseTestCase):

    def test_add_book_shelf_403_permission_not_found(self):
        res = self.client.post('/book', headers=self._get_headers(["test:post"]))
        self.assert_error(res, expect_status_code=403, expect_message='Permission not found.')

    def test_add_book_shelf_200_with_correct_payload(self):
        payload = {
            "isbn13": "9781234567897",
            "title": "Test Book",
            "authors": ["Author 1"],
            "image": "book1.jpg",
            "shelf": "read"
        }
        res = self.client.post('/book', json=payload, headers=self._get_headers(["book:add_to_shelf"]))
        self.assertEqual(200, res.status_code)
        print(res.get_json().get('book'))
        self.assertDictEqual(BookResponse.from_json(payload).to_dict(), res.get_json().get('book'))

    def test_add_book_shelf_returns_422_Unprocessable_due_to_missing_payload(self):
        res = self.client.post('/book',
                               content_type='application/json',
                               headers=self._get_headers(["book:add_to_shelf"]))
        expected_message = 'Unprocessable: 422 Unprocessable Entity: The request was well-formed but was unable to be followed due to semantic errors.'
        self.assert_error(res, expect_status_code=422,
                          expect_message=expected_message)

    def test_fetch_book_403_permission_not_found(self):
        res = self.client.get('/book/1234567890', headers=self._get_headers(["test:get"]))
        self.assert_error(res, expect_status_code=403, expect_message='Permission not found.')

    def test_fetch_book_200_with_correct_payload(self):
        mock_book = BookResponse(
            isbn13='9780061120084',
            isbn10=None,
            title='Test Title',
            authors=['Test Author'],
            image='Test Image',
            shelf='Test Shelf',
        )

        self.mock_book_service.mock_books([mock_book])

        res = self.client.get(f'/book/{mock_book.isbn13}', headers=self._get_headers(["book:get_details"]))
        self.assertEqual(200, res.status_code)
        print(res.get_json())

        self.assertDictEqual(mock_book.to_dict(), res.get_json().get('book'))

    def test_fetch_book_404_not_found_due_to_missing_book_id(self):
        res = self.client.get('/book/', headers=self._get_headers(["book:get_details"]))
        self.assert_error(res, expect_status_code=404, expect_message='Not found')

    # @shelf_bp.route('/book/<string:book_id>', methods=['DELETE'])
    # @requires_auth('book:delete_shelf')
    # def delete_book(payload, book_id: str):
    #     user_id = payload.get('sub')
    #     return remove_book(user_id=user_id, book_id=book_id)
    # test 403_permission_not_found
    def test_delete_book_403_permission_not_found(self):
        res = self.client.delete('/book/1234567890', headers=self._get_headers(["test:delete"]))
        self.assert_error(res, expect_status_code=403, expect_message='Permission not found.')

    # test 200 with correct payload and book_id
    # test missing book_id 422 not book existing
    def test_delete_book_200_with_correct_payload(self):
        mock_book = BookResponse(
            isbn13='9780061120084',
            isbn10=None,
            title='Test Title',
            authors=['Test Author'],
            image='Test Image',
            shelf='read',
        )

        self.client.post('/book', json=mock_book.to_dict(), headers=self._get_headers(["book:add_to_shelf"]))

        res = self.client.delete(f'/book/{mock_book.isbn13}', headers=self._get_headers(["book:delete_shelf"]))
        self.assertEqual(200, res.status_code)
        self.assertEqual(mock_book.isbn13, res.get_json().get('deleted'))

    def test_delete_book_404_not_found_due_to_missing_book_id(self):
        res = self.client.delete('/book/9780061120084', headers=self._get_headers(["book:delete_shelf"]))
        self.assert_error(res, expect_status_code=404, expect_message='Not found')

    # @shelf_bp.route('/book/<string:book_id>', methods=['PATCH'])
    # @requires_auth('book:update_shelf')
    # def patch_book_shelf(payload, book_id: str):
    #     user_id = payload.get('sub')
    #     return update_book_shelf(user_id=user_id, book_id=book_id, request=request)
    # test 403_permission_not_found
    # test 200 with correct payload and book_id
    # test missing book_id 422 not book existing


if __name__ == '__main__':
    unittest.main()
