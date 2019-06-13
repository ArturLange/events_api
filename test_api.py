import json
import os
import tempfile
import unittest
from datetime import datetime, timedelta

from database import db
from events_api_app import app
from init_db import add_events
from models import Reservation, Ticket, TicketType
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
            "Premium": 10,
            "Regular": 5
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected)

    def test_get_tickets_info_not_found(self):
        expected = {
            'error': 'Event not found'
        }
        response = self.client.get('/events/11111/tickets')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, expected)

    def test_ticket_reservation(self):
        expected_before = {
            "Premium": 10,
            "Regular": 5
        }
        expected_after = {
            "Premium": 9,
            "Regular": 5
        }
        response = self.client.get('/events/1/tickets')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected_before)

        self.client.post(
            '/events/1/reservations',
            json=({"ticket_type": "Premium"})
        )

        response = self.client.get('/events/1/tickets')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected_after)

    def test_ticket_reservation_event_not_found(self):
        expected = {
            'error': 'Event not found'
        }
        response = self.client.post(
            '/events/11111/reservations',
            json=({"ticket_type": "Premium"})
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, expected)

    def test_ticket_reservation_invalid_ticket_type(self):
        expected = {
            'error': 'Event has no tickets of given type'
        }
        response = self.client.post(
            '/events/1/reservations',
            json=({"ticket_type": "WeirdTicketType"})
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, expected)

    def test_ticket_reservation_all_tickets_reserved(self):
        expected = {
            'error': 'No tickets available'
        }
        response = self.client.post(
            '/events/2/reservations',
            json=({"ticket_type": "VIP"})
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, expected)


if __name__ == "__main__":
    unittest.main()
