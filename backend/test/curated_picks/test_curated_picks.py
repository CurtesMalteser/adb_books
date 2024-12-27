"""
Module for testing the Curated Picks endpoints.
"""
import json
import unittest

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

        list_data = res.get_json().get('list')
        description = list_data.get('description')
        name = list_data.get('name')
        list_id = list_data.get('id')
        self.assertEqual('Test Description', description)
        self.assertEqual('Test List', name)
        self.assertTrue(list_id)
        self.assertEqual(201, res.status_code)

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

if __name__ == '__main__':
    unittest.main()
