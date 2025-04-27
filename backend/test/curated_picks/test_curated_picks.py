"""
Module for testing the Curated Picks endpoints.
"""
import json
import unittest

from app.models.book_dto import BookResponse
from app.models.curated_list import CuratedList
from app.models.curated_pick import CuratedPick
from test.base_test_case import BaseTestCase


class CuratedPicksTestCase(BaseTestCase):
    """Tests for the Curated Picks endpoints."""

    @staticmethod
    def _setup_curated_lists():
        CuratedList(name='Test List', description='Test Description').insert()
        CuratedList(name='Test List 2', description='Test Description 2').insert()

    @staticmethod
    def _setup_curated_picks():
        CuratedPick(list_id=1, isbn13="9780061120084", position=3, isbn10=None).insert()
        CuratedPick(list_id=1, isbn13=None, position=1, isbn10="0471958697").insert()
        CuratedPick(list_id=2, isbn13="9780061120086", position=2, isbn10="1471958697").insert()

    @staticmethod
    def _mock_books():
        return [
            BookResponse(
                isbn13='9780061120084',
                isbn10=None,
                title='Test Title',
                authors=['Test Author'],
                image='Test Image',
                shelf='Test Shelf',
            ),
            BookResponse(
                isbn13=None,
                isbn10='0471958697',
                title='Test Title 2',
                authors=['Test Author 2'],
                image='Test Image 2',
                shelf='Test Shelf 2',
            ),
        ]

    def test_post_curated_list_returns_201(self):
        payload = {
            "name": "Test List",
            "description": "Test Description"
        }

        res = self.client.post(
            '/curated-list',
            data=json.dumps(payload),
            content_type='application/json',
            headers=self._get_headers(["booklist:curator"])
        )

        self.assertEqual(201, res.status_code)
        list_data = res.get_json().get('list')
        description = list_data.get('description')
        name = list_data.get('name')
        list_id = list_data.get('id')
        self.assertEqual('Test Description', description)
        self.assertEqual('Test List', name)
        self.assertTrue(list_id)

    def test_post_curated_list_returns_403_permission_not_found(self):
        payload = {
            "name": "Test List",
            "description": "Test Description"
        }

        res = self.client.post(
            '/curated-list',
            data=json.dumps(payload),
            content_type='application/json',
            headers=self._get_headers(["booklist:get"])
        )

        self.assert_error(res, expect_status_code=403, expect_message='Permission not found.')

    def test_fetch_curated_lists_returns_empty_list_code_200(self):
        res = self.client.get('/curated-lists', headers=self._get_headers(["booklist:get"]))
        self.assertEqual(200, res.status_code)
        list_data = res.get_json().get('lists')
        self.assertEqual(len(list_data), 0)

    def test_fetch_curated_lists_returns_code_200(self):
        self.with_context(self._setup_curated_lists)
        res = self.client.get('/curated-lists', headers=self._get_headers(["booklist:get"]))
        self.assertEqual(200, res.status_code)
        list_data = res.get_json().get('lists')
        self.assertEqual(len(list_data), 2)

    def test_fetch_curated_lists_returns_400_invalid_claims_missing_permissions(self):
        headers = {
            "Authorization": 'Bearer {"sub": "auth0|test_user"}'
        }

        res = self.client.get('/curated-lists', headers=headers)
        self.assert_error(res, expect_status_code=400, expect_message='Permissions not included in JWT.')

    def test_post_curated_pick_returns_201_isbn13(self):
        payload = {
            "list_id": "1",
            "position": "3",
            "isbn13": "9780061120084",
        }

        self.with_context(self._setup_curated_lists)

        res = self.client.post(
            '/curated-pick',
            data=json.dumps(payload),
            content_type='application/json',
            headers=self._get_headers(["booklist:curator"])
        )

        self.assertEqual(201, res.status_code)
        curated_pick_data = res.get_json().get('pick')
        list_id = curated_pick_data.get('list_id')
        position = curated_pick_data.get('position')
        isbn13 = curated_pick_data.get('isbn13')
        self.assertEqual(1, list_id)
        self.assertEqual(3, position)
        self.assertEqual("9780061120084", isbn13)

    def test_post_curated_pick_returns_201_isbn10(self):
        payload = {
            "list_id": "1",
            "position": "2",
            "isbn10": "123456789X",
        }

        self.with_context(self._setup_curated_lists)

        res = self.client.post(
            '/curated-pick',
            data=json.dumps(payload),
            content_type='application/json',
            headers=self._get_headers(["booklist:curator"])
        )

        self.assertEqual(201, res.status_code)
        curated_pick_data = res.get_json().get('pick')
        list_id = curated_pick_data.get('list_id')
        position = curated_pick_data.get('position')
        isbn10 = curated_pick_data.get('isbn10')
        self.assertEqual(1, list_id)
        self.assertEqual(2, position)
        self.assertEqual("123456789X", isbn10)

    def test_post_curated_pick_returns_422_bad_request_missing_isbn(self):
        def add_picked_lists():
            """
            Add some CuratedList's to the database.
            """
            CuratedList(name='Test List', description='Test Description').insert()

        payload = {
            "list_id": "1",
            "position": "3",
        }

        self.with_context(add_picked_lists)

        res = self.client.post(
            '/curated-pick',
            data=json.dumps(payload),
            content_type='application/json',
            headers=self._get_headers(["booklist:curator"])
        )

        expected_message = "At least one of 'isbn10' or 'isbn13' must be provided."
        self.assert_error(res, expect_status_code=422, expect_message=expected_message)

    def test_post_curated_pick_returns_403_permission_not_found(self):
        payload = {
            "list_id": "1",
            "position": "3",
            "isbn10": "0471958697",
        }

        self.with_context(self._setup_curated_lists)

        res = self.client.post(
            '/curated-pick',
            data=json.dumps(payload),
            content_type='application/json',
            headers=self._get_headers(["booklist:get"])
        )

        self.assert_error(res, expect_status_code=403, expect_message='Permission not found.')

    def test_post_curated_pick_returns_409_entry_already_exists(self):
        def add_picked_entries():
            """
            Add some CuratedList's to the database.
            """
            self._setup_curated_lists()
            self._setup_curated_picks()

        payload = {
            "list_id": "1",
            "position": "3",
            "isbn13": "9780061120084",
        }

        self.with_context(add_picked_entries)

        res = self.client.post(
            '/curated-pick',
            data=json.dumps(payload),
            content_type='application/json',
            headers=self._get_headers(["booklist:curator"])
        )

        expected_message = "Curated pick 'CuratedPick(list_id=1, isbn13=9780061120084, isbn10=None, position=3)' already exists, Try PUT to update."
        self.assert_error(res, expect_status_code=409, expect_message=expected_message)

    def test_fetch_curated_picks_returns_code_200(self):
        def add_picked_entries():
            """
            Add some CuratedList's to the database.
            """
            self._setup_curated_lists()
            self._setup_curated_picks()

        self.mock_book_service.mock_books(self._mock_books())

        self.with_context(add_picked_entries)
        res = self.client.get('/curated-picks?list_id=1', headers=self._get_headers(["booklist:get"]))
        self.assertEqual(200, res.status_code)
        picks_data = res.get_json().get('books')
        books = [BookResponse.from_json(d=book) for book in picks_data]
        self.assertListEqual(self._mock_books(), books)

    def test_fetch_curated_picks_returns_code_404_list_does_not_exist(self):
        self.with_context(self._setup_curated_lists)
        res = self.client.get('/curated-picks?list_id=3', headers=self._get_headers(["booklist:get"]))
        self.assert_error(res, expect_status_code=404, expect_message='The specified list does not exist.')

    def test_fetch_curated_picks_returns_code_404_list_id_param_not_provided(self):
        res = self.client.get('/curated-picks', headers=self._get_headers(["booklist:get"]))
        self.assert_error(res, expect_status_code=404, expect_message='List ID is required.')

    def test_fetch_curated_picks_returns_403_permission_not_found(self):
        res = self.client.get('/curated-picks?list_id=1', headers=self._get_headers(["booklist:put"]))
        self.assert_error(res, expect_status_code=403, expect_message='Permission not found.')

    def test_put_curated_list_returns_403_permission_not_found(self):
        payload = {
            "name": "Test List",
            "description": "Test Description"
        }

        res = self.client.put(
            '/curated-list',
            data=json.dumps(payload),
            content_type='application/json',
            headers=self._get_headers(["booklist:get"])
        )

        self.assert_error(res, expect_status_code=403, expect_message='Permission not found.')

    def test_put_curated_list_returns_200(self):
        payload = {
            "id": "1",
            "name": "Favorite curator books",
            "description": "The books that I most enjoyed reading"
        }

        self.with_context(self._setup_curated_lists)

        res = self.client.put(
            '/curated-list',
            data=json.dumps(payload),
            content_type='application/json',
            headers=self._get_headers(["booklist:curator"])
        )

        self.assertEqual(200, res.status_code)
        list_data = res.get_json().get('list')
        description = list_data.get('description')
        name = list_data.get('name')
        list_id = list_data.get('id')
        self.assertEqual('The books that I most enjoyed reading', description)
        self.assertEqual('Favorite curator books', name)
        self.assertTrue(list_id)

    def test_put_curated_list_returns_404_no_such_pick_list(self):
        list_id = 1_000_000
        payload = {
            "id": str(list_id),
            "name": "Favorite curator books",
            "description": "The books that I most enjoyed reading"
        }

        self.with_context(self._setup_curated_lists)

        res = self.client.put(
            '/curated-list',
            data=json.dumps(payload),
            content_type='application/json',
            headers=self._get_headers(["booklist:curator"])
        )

        expect_message = f"Curated list with ID '{list_id}' does not exist."
        self.assert_error(res, expect_status_code=404, expect_message=expect_message)

    def test_delete_curated_list_returns_403_permission_not_found(self):
        self.with_context(self._setup_curated_lists)

        res = self.client.delete('/curated-list/1', headers=self._get_headers(["booklist:get"]))
        self.assert_error(res, expect_status_code=403, expect_message='Permission not found.')

    def test_delete_curated_list_returns_204(self):
        self.with_context(self._setup_curated_lists)
        res = self.client.delete('/curated-list/1', headers=self._get_headers(["booklist:curator"]))
        self.assertEqual(204, res.status_code)

    def test_delete_curated_list_returns_404(self):
        self.with_context(self._setup_curated_lists)
        res = self.client.delete('/curated-list/1000000', headers=self._get_headers(["booklist:curator"]))
        self.assert_error(res, expect_status_code=404, expect_message='The specified list does not exist.')

    def test_delete_curated_pick_returns_403_permission_not_found(self):
        self.with_context(self._setup_curated_lists)
        res = self.client.delete('/curated-pick/1', headers=self._get_headers(["booklist:get"]))
        self.assert_error(res, expect_status_code=403, expect_message='Permission not found.')

    def test_delete_curated_pick_returns_204(self):
        def add_picked_entries():
            """
            Add some CuratedList's to the database.
            """
            self._setup_curated_lists()
            self._setup_curated_picks()

        self.mock_book_service.mock_books(self._mock_books())

        self.with_context(add_picked_entries)

        res = self.client.delete('/curated-pick/9780061120084', headers=self._get_headers(["booklist:curator"]))
        self.assertEqual(204, res.status_code)

    def test_delete_curated_pick_returns_404_no_such_pick(self):
        self.with_context(self._setup_curated_lists)
        pick_id = 9780061120084
        res = self.client.delete(f"/curated-pick/{pick_id}", headers=self._get_headers(["booklist:curator"]))
        expect_message = f"The specified pick ID:'{pick_id}' does not exist."
        self.assert_error(res, expect_status_code=404, expect_message=expect_message)

    def test_delete_curated_pick_returns_404_invalid_pick_id(self):
        self.with_context(self._setup_curated_lists)
        pick_id = 1_000_000
        res = self.client.delete(f"/curated-pick/{pick_id}", headers=self._get_headers(["booklist:curator"]))
        expect_message = f"Incorrect pick ID format:'{pick_id}'. ISBN10 or ISBN13 expected."
        self.assert_error(res, expect_status_code=404, expect_message=expect_message)

    def test_put_curated_pick_returns_403_permission_not_found(self):
        payload = {
            "position": "3",
        }

        self.with_context(self._setup_curated_lists)

        res = self.client.patch(
            '/curated-pick/9780061120084',
            data=json.dumps(payload),
            content_type='application/json',
            headers=self._get_headers(["booklist:get"])
        )

        self.assert_error(res, expect_status_code=403, expect_message='Permission not found.')

    def test_patch_curated_pick_returns_200_when_moving_book_down_in_ranking(self):
        def add_picked_entries():
            """
            Add some CuratedList's to the database.
            """
            mock_books = {
                i: BookResponse(
                    isbn13=isbn13,
                    isbn10=isbn10,
                    title="Dummy Title",
                    authors=["John Doe"],
                    image="",
                    shelf=None
                )
                for i, (isbn13, isbn10) in enumerate([
                    ("9780061120084", "0061120081"),  # This book will be moved to third position
                    ("9789231781766", "5476128581"),  # This book will be moved to first position
                    ("9783648388211", "5551926079"),
                    ("9789499642106", "1438509057"),
                    ("9787717178017", "7429530850")
                ], start=1)
            }

            self._setup_curated_lists()
            for book_position, book in mock_books.items():
                CuratedPick(list_id=2, isbn13=book.isbn13, position=book_position, isbn10=book.isbn10).insert()

            self.mock_book_service.mock_books(list(mock_books.values()))

        self.with_context(add_picked_entries)

        payload = {
            "position": 3,
        }

        res = self.client.patch(
            '/curated-pick/9780061120084',
            data=json.dumps(payload),
            content_type='application/json',
            headers=self._get_headers(["booklist:curator"])
        )

        self.assertEqual(200, res.status_code)
        pick_data = res.get_json().get('pick')
        position = pick_data.get('position')
        self.assertEqual(3, position)
        # Confirm book in second position has been moved to first position
        res = self.client.get('/curated-picks?list_id=2', headers=self._get_headers(["booklist:get"]))
        self.assertEqual(200, res.status_code)
        picks_data = res.get_json().get('books')
        pick_in_first = next((pick for pick in picks_data if pick['isbn13'] == "9789231781766"), None)
        self.assertEqual(1, pick_in_first.get('position'))

    def test_put_curated_pick_returns_200_when_moving_book_up_in_ranking(self):
        def add_picked_entries():
            """
            Add some CuratedList's to the database.
            """
            mock_books = {
                i: BookResponse(
                    isbn13=isbn13,
                    isbn10=isbn10,
                    title="Dummy Title",
                    authors=["John Doe"],
                    image="",
                    shelf=None
                )
                for i, (isbn13, isbn10) in enumerate([
                    ("9780061120084", "0061120081"),
                    ("9789231781766", "5476128581"),
                    ("9783648388211", "5551926079"),
                    ("9789499642106", "1438509057"),  # This book will be moved to fifth position
                    ("9787717178017", "7429530850")  # This book will be moved to second position
                ], start=1)
            }

            self._setup_curated_lists()
            for book_position, book in mock_books.items():
                print(f'position: {book_position}, isbn13: {book.isbn13}, isbn10: {book.isbn10}')
                CuratedPick(list_id=2, isbn13=book.isbn13, position=book_position, isbn10=book.isbn10).insert()

            self.mock_book_service.mock_books(list(mock_books.values()))

        self.with_context(add_picked_entries)

        payload = {
            "position": 2,
        }

        res = self.client.patch(
            '/curated-pick/7429530850',
            data=json.dumps(payload),
            content_type='application/json',
            headers=self._get_headers(["booklist:curator"])
        )

        self.assertEqual(200, res.status_code)
        pick_data = res.get_json().get('pick')
        position = pick_data.get('position')
        self.assertEqual(2, position)
        # Confirm book in fourth position has been moved to fifth position
        res = self.client.get('/curated-picks?list_id=2', headers=self._get_headers(["booklist:get"]))
        self.assertEqual(200, res.status_code)
        picks_data = res.get_json().get('books')
        pick_in_first = next((pick for pick in picks_data if pick['isbn10'] == "1438509057"), None)
        self.assertEqual(5, pick_in_first.get('position'))

    def test_patch_curated_pick_returns_404_no_such_pick(self):
        self.with_context(self._setup_curated_lists)
        pick_id = 9780061120084
        payload = {
            "position": 3,
        }

        res = self.client.patch(
            f"/curated-pick/{pick_id}",
            data=json.dumps(payload),
            content_type='application/json',
            headers=self._get_headers(["booklist:curator"])
        )

        expect_message = f"The specified pick ID:'{pick_id}' does not exist."
        self.assert_error(res, expect_status_code=404, expect_message=expect_message)

    def test_patch_curated_pick_returns_400_invalid_position(self):
        payload = {
            "position": 0,
        }

        res = self.client.patch(
            '/curated-pick/9780061120084',
            data=json.dumps(payload),
            content_type='application/json',
            headers=self._get_headers(["booklist:curator"])
        )

        expect_message = "Invalid position value."
        self.assert_error(res, expect_status_code=400, expect_message=expect_message)


if __name__ == '__main__':
    unittest.main()
