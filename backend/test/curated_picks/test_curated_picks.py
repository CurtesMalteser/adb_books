"""
Module for testing the Curated Picks endpoints.
"""
import json
import unittest

from app.models.book_dto import db
from app.models.curated_list import CuratedList
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

        self.with_context(add_picked_lists)

        headers = {
            "Authorization": 'Bearer {"sub": "auth0|test_user", "permissions": ["booklist:get"]}'
        }

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


if __name__ == '__main__':
    unittest.main()
