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


if __name__ == "__main__":
    app.run()
