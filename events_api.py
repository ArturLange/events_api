import json
from datetime import datetime

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/events")
def get_events():
    return jsonify([
        {
            "name": "Woodstock Festival",
            "start_time": datetime(1999, 7, 23, 12).isoformat(),
            "end_time": datetime(1999, 7, 25, 12).isoformat(),
            "ticket_types": ["VIP"],
        },
        {
            "name": "Cirque du Soleil",
            "start_time": datetime(2019, 10, 23, 20, 0).isoformat(),
            "end_time": datetime(2019, 10, 23, 23, 0).isoformat(),
            "ticket_types": ["VIP", "Regular", "Premium"],
        },
    ])


@app.route("/events/<int:event_id>/tickets")
def get_tickets(event_id):
    return jsonify({
        "VIP": 25,
        "Regular": 32,
        "Premium": 120
    })


@app.route("/events/<int:event_id>/reservations", methods=["POST"])
def ticket_reservation():
    return jsonify({
        'token': 'ca78fd642f5f655a09b67c0b0f34612c'
    })


@app.route("/events/<int:event_id>/reservations/<reservation_token>")
def get_reservation(event_id, reservation_token):
    return jsonify({
        "paid": False,
        "event": {
            "name": "Woodstock Festival",
            "start_time": datetime(1999, 7, 23, 12).isoformat(),
            "end_time": datetime(1999, 7, 25, 12).isoformat(),
            "ticket_types": ["VIP"],
        },
        "ticket_type": "VIP"
    })


@app.route("/events/<int:event_id>/reservations/<reservation_token>/pay", methods=["POST"])
def pay_for_reservation(event_id, reservation_token):
    return jsonify({
        "paid": True,
        "event": {
            "name": "Woodstock Festival",
            "start_time": datetime(1999, 7, 23, 12).isoformat(),
            "end_time": datetime(1999, 7, 25, 12).isoformat(),
            "ticket_types": ["VIP"],
        },
        "ticket_type": "VIP"
    })


@app.route("/stats")
def get_stats():
    return jsonify({})


if __name__ == "__main__":
    app.run()
