"""
Module for testing the Curated Picks endpoints.
"""
import json
import unittest

from app.models.book_dto import db
from app.models.curated_list import CuratedList
from app.models.curated_pick import CuratedPick
from test.base_test_case import BaseTestCase


class CuratedPicksTestCase(BaseTestCase):
    """Tests for the Curated Picks endpoints."""

    def test_post_curated_list_returns_201(self):
        payload = {
            "name": "Test List",
            "description": "Test Description"
        }

        headers = {
            "Authorization": 'Bearer {"sub": "auth0|test_user", "permissions": ["booklist:curator"]}'
        }

        res = self.client.post(
            '/curated-list',
            data=json.dumps(payload),
            content_type='application/json',
            headers=headers
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

        headers = {
            "Authorization": 'Bearer {"sub": "auth0|test_user", "permissions": ["booklist:get"]}'
        }

        res = self.client.post(
            '/curated-list',
            data=json.dumps(payload),
            content_type='application/json',
            headers=headers
        )

        self.assertEqual(403, res.status_code)
        message = res.get_json().get('message')
        self.assertEqual('Permission not found.', message)

    def test_fetch_curated_lists_returns_empty_list_code_200(self):
        headers = {
            "Authorization": 'Bearer {"sub": "auth0|test_user", "permissions": ["booklist:get"]}'
        }

        res = self.client.get('/curated-lists', headers=headers)
        self.assertEqual(200, res.status_code)
        list_data = res.get_json().get('lists')
        self.assertEqual(len(list_data), 0)

    def test_fetch_curated_lists_returns_code_200(self):
        def add_picked_lists():
            """
            Add some CuratedList's to the database.
            """
            CuratedList(name='Test List', description='Test Description').insert()
            CuratedList(name='Test List 2', description='Test Description 2').insert()
            db.session.close()

        headers = {
            "Authorization": 'Bearer {"sub": "auth0|test_user", "permissions": ["booklist:get"]}'
        }

        self.with_context(add_picked_lists)
        res = self.client.get('/curated-lists', headers=headers)
        self.assertEqual(200, res.status_code)
        list_data = res.get_json().get('lists')
        self.assertEqual(len(list_data), 2)

    def test_fetch_curated_lists_returns_400_invalid_claims_missing_permissions(self):
        headers = {
            "Authorization": 'Bearer {"sub": "auth0|test_user"}'
        }

        res = self.client.get('/curated-lists', headers=headers)
        self.assertEqual(400, res.status_code)
        message = res.get_json().get('message')
        self.assertEqual('Permissions not included in JWT.', message)

    def test_post_curated_pick_returns_201_isbn_13(self):
        def add_picked_lists():
            """
            Add some CuratedList's to the database.
            """
            CuratedList(name='Test List', description='Test Description').insert()
            CuratedList(name='Test List 2', description='Test Description 2').insert()
            db.session.close()

        payload = {
            "list_id": "1",
            "position": "3",
            "isbn_13": "9780061120084",
        }

        headers = {
            "Authorization": 'Bearer {"sub": "auth0|test_user", "permissions": ["booklist:curator"]}'
        }

        self.with_context(add_picked_lists)

        res = self.client.post(
            '/curated-pick',
            data=json.dumps(payload),
            content_type='application/json',
            headers=headers
        )

        self.assertEqual(201, res.status_code)
        curated_pick_data = res.get_json().get('pick')
        list_id = curated_pick_data.get('list_id')
        position = curated_pick_data.get('position')
        isbn_13 = curated_pick_data.get('isbn_13')
        self.assertEqual(1, list_id)
        self.assertEqual(3, position)
        self.assertEqual("9780061120084", isbn_13)

    def test_post_curated_pick_returns_201_isbn_10(self):
        def add_picked_lists():
            """
            Add some CuratedList's to the database.
            """
            CuratedList(name='Test List', description='Test Description').insert()
            CuratedList(name='Test List 2', description='Test Description 2').insert()
            db.session.close()

        payload = {
            "list_id": "1",
            "position": "2",
            "isbn_10": "123456789X",
        }

        headers = {
            "Authorization": 'Bearer {"sub": "auth0|test_user", "permissions": ["booklist:curator"]}'
        }

        self.with_context(add_picked_lists)

        res = self.client.post(
            '/curated-pick',
            data=json.dumps(payload),
            content_type='application/json',
            headers=headers
        )

        self.assertEqual(201, res.status_code)
        curated_pick_data = res.get_json().get('pick')
        list_id = curated_pick_data.get('list_id')
        position = curated_pick_data.get('position')
        isbn_10 = curated_pick_data.get('isbn_10')
        self.assertEqual(1, list_id)
        self.assertEqual(2, position)
        self.assertEqual("123456789X", isbn_10)

    def test_post_curated_pick_returns_422_bad_request_missing_isbn(self):
        def add_picked_lists():
            """
            Add some CuratedList's to the database.
            """
            CuratedList(name='Test List', description='Test Description').insert()
            db.session.close()

        payload = {
            "list_id": "1",
            "position": "3",
        }

        headers = {
            "Authorization": 'Bearer {"sub": "auth0|test_user", "permissions": ["booklist:curator"]}'
        }

        self.with_context(add_picked_lists)

        res = self.client.post(
            '/curated-pick',
            data=json.dumps(payload),
            content_type='application/json',
            headers=headers
        )

        self.assertEqual(422, res.status_code)
        message = res.get_json().get('message')
        self.assertEqual("At least one of 'isbn_10' or 'isbn_13' must be provided.", message)

    def test_post_curated_pick_returns_403_permission_not_found(self):
        def add_picked_lists():
            """
            Add some CuratedList's to the database.
            """
            CuratedList(name='Test List', description='Test Description').insert()
            db.session.close()

        payload = {
            "list_id": "1",
            "position": "3",
            "isbn_10": "0471958697",
        }

        headers = {
            "Authorization": 'Bearer {"sub": "auth0|test_user", "permissions": ["booklist:get"]}'
        }

        self.with_context(add_picked_lists)

        res = self.client.post(
            '/curated-pick',
            data=json.dumps(payload),
            content_type='application/json',
            headers=headers
        )

        self.assertEqual(403, res.status_code)
        message = res.get_json().get('message')
        self.assertEqual('Permission not found.', message)

    def test_post_curated_pick_returns_409_entry_already_exists(self):
        def add_picked_entries():
            """
            Add some CuratedList's to the database.
            """
            CuratedList(name='Test List', description='Test Description').insert()
            CuratedPick(list_id=1, isbn_13="9780061120084", position=3, isbn_10=None).insert()
            db.session.close()

        payload = {
            "list_id": "1",
            "position": "3",
            "isbn_13": "9780061120084",
        }

        headers = {
            "Authorization": 'Bearer {"sub": "auth0|test_user", "permissions": ["booklist:curator"]}'
        }

        self.with_context(add_picked_entries)

        res = self.client.post(
            '/curated-pick',
            data=json.dumps(payload),
            content_type='application/json',
            headers=headers
        )

        self.assertEqual(409, res.status_code)
        message = res.get_json().get('message')
        expected_message = "Curated pick 'CuratedPick(list_id=1, isbn_13=9780061120084, isbn_10=None, position=3)' already exists, Try PUT to update."
        self.assertEqual(expected_message, message)

    def test_fetch_curated_picks_returns_code_200(self):
        def add_picked_entries():
            """
            Add some CuratedList's to the database.
            """
            CuratedList(name='Test List', description='Test Description').insert()
            CuratedList(name='Test List 2', description='Test Description 2').insert()
            CuratedPick(list_id=1, isbn_13="9780061120084", position=3, isbn_10=None).insert()
            CuratedPick(list_id=1, isbn_13="9780061120084", position=1, isbn_10="0471958697").insert()
            CuratedPick(list_id=2, isbn_13="9780061120085", position=2, isbn_10="1471958697").insert()
            db.session.close()

        expected_picks = [
            {'id': None, 'isbn_13': '9780061120084', 'list_id': 1, 'position': 3},
            {'id': None, 'isbn_10': '0471958697', 'isbn_13': '9780061120084', 'list_id': 1, 'position': 1}
        ]

        headers = {
            "Authorization": 'Bearer {"sub": "auth0|test_user", "permissions": ["booklist:get"]}'
        }

        self.with_context(add_picked_entries)
        res = self.client.get('/curated-picks?list_id=1', headers=headers)
        self.assertEqual(200, res.status_code)
        picks_data = res.get_json().get('picks')

        self.assertListEqual(expected_picks, picks_data)

    def test_fetch_curated_picks_returns_code_404_list_does_not_exist(self):
        def add_picked_entries():
            """
            Add some CuratedList's to the database.
            """
            CuratedList(name='Test List', description='Test Description').insert()
            CuratedList(name='Test List 2', description='Test Description 2').insert()
            db.session.close()

        headers = {
            "Authorization": 'Bearer {"sub": "auth0|test_user", "permissions": ["booklist:get"]}'
        }

        self.with_context(add_picked_entries)
        res = self.client.get('/curated-picks?list_id=3', headers=headers)
        self.assertEqual(404, res.status_code)
        message = res.get_json().get('message')
        self.assertEqual('The specified list does not exist.', message)

    def test_fetch_curated_picks_returns_code_404_list_id_param_not_provided(self):
        headers = {
            "Authorization": 'Bearer {"sub": "auth0|test_user", "permissions": ["booklist:get"]}'
        }

        res = self.client.get('/curated-picks', headers=headers)
        self.assertEqual(404, res.status_code)
        message = res.get_json().get('message')
        self.assertEqual('List ID is required.', message)

    def test_fetch_curated_picks_returns_403_permission_not_found(self):
        headers = {
            "Authorization": 'Bearer {"sub": "auth0|test_user", "permissions": ["booklist:put"]}'
        }

        res = self.client.get('/curated-picks?list_id=1', headers=headers)
        self.assertEqual(403, res.status_code)
        message = res.get_json().get('message')
        self.assertEqual('Permission not found.', message)


if __name__ == '__main__':
    unittest.main()
