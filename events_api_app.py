import json
from datetime import datetime, timedelta

from flask import Flask, jsonify, request
from sqlalchemy.orm.query import Query

from database import db_session
from models import Event, Reservation, Ticket, TicketType

app = Flask(__name__)


def get_available_tickets(ticket_type_id: int) -> Query:
    return db_session.query(Ticket).filter_by(
        ticket_type_id=ticket_type_id).filter(~Ticket.reservations.any(Reservation.end_time > datetime.utcnow()))


@app.route("/events")
def get_events():
    events = [event.to_dict() for event in Event.query.all()]
    return jsonify(events)


@app.route("/events/<int:event_id>/tickets")
def get_tickets(event_id):
    ticket_types = db_session.query(
        TicketType).filter_by(event_id=event_id).filter(TicketType.tickets.any()).all()
    response = {
        ticket_type.name: get_available_tickets(ticket_type.id).count()
        for ticket_type in ticket_types
    }
    return jsonify(response)


@app.route("/events/<int:event_id>/reservations", methods=["POST"])
def ticket_reservation(event_id):
    ticket_type_id = db_session.query(TicketType.id).filter_by(
        event_id=event_id).filter_by(name=request.json['ticket_type']).first()[0]
    ticket = get_available_tickets(ticket_type_id).first()
    reservation = Reservation(
        end_time=datetime.utcnow() + timedelta(minutes=15),
        ticket=ticket
    )
    db_session.add(reservation)
    db_session.commit()
    return jsonify({
        'token': ticket.token
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
