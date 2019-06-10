import json
from datetime import datetime

from flask import Flask, jsonify

from database import db_session
from models import Event, Ticket, TicketType

app = Flask(__name__)


@app.route("/events")
def get_events():
    events = [event.to_dict() for event in Event.query.all()]
    return jsonify(events)


@app.route("/events/<int:event_id>/tickets")
def get_tickets(event_id):
    ticket_types = db_session.query(
        TicketType).filter_by(event_id=event_id).filter(TicketType.tickets.any()).all()
    response = {
        ticket_type.name: db_session.query(Ticket).filter_by(
            ticket_type_id=ticket_type.id).count()
        for ticket_type in ticket_types
    }
    return jsonify(response)


@app.route("/events/<int:event_id>/reservations", methods=["POST"])
def ticket_reservation(event_id):
    return jsonify({
        'token': '8ba44193-cffa-4e32-a4e4-625a0dd72cd3'
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
    app.run(debug=True)
