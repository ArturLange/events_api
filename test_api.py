import os
import tempfile
import unittest

from database import db
from events_api_app import app
from init_db import add_events
from settings import TEST_SQLALCHEMY_DATABASE_URI


class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = TEST_SQLALCHEMY_DATABASE_URI
        app.testing = True
        self.client = app.test_client()
        with app.app_context():
            db.create_all()
            add_events()

    def tearDown(self):
        with app.app_context():
            db.drop_all()


class TestAPI(TestCase):

    def test_get_events(self):
        response = self.client.get('/events')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)

    def test_get_tickets_info(self):
        response = self.client.get('/events/1/tickets')
        expected = {
            "Premium": 120,
            "Regular": 250
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected)


if __name__ == "__main__":
    unittest.main()
