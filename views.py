import json
from datetime import datetime, timedelta

from flask import Flask, Response, abort, jsonify, request
from sqlalchemy.orm.query import Query
from sqlalchemy.sql.expression import literal

from database import db
from models import Event, Reservation, Ticket, TicketType


def get_available_tickets(ticket_type_id: int) -> Query:
    return db.session.query(Ticket).filter_by(
        ticket_type_id=ticket_type_id).filter(~Ticket.reservations.any(Reservation.end_time > datetime.utcnow()))


def get_events() -> Response:
    events = [event.to_dict() for event in Event.query.all()]
    return jsonify(events)


def get_tickets(event_id) -> Response:
    event_exists = db.session.query(Event).filter_by(id=event_id).count() > 0
    if not event_exists:
        return abort(404)
    ticket_types = db.session.query(
        TicketType).filter_by(event_id=event_id).filter(TicketType.tickets.any()).all()
    response = {
        ticket_type.name: get_available_tickets(ticket_type.id).count()
        for ticket_type in ticket_types
    }
    return jsonify(response)


def ticket_reservation(event_id) -> Response:
    ticket_type_id = db.session.query(TicketType.id).filter_by(
        event_id=event_id).filter_by(name=request.json['ticket_type']).first()[0]
    ticket = get_available_tickets(ticket_type_id).first()
    reservation = Reservation(
        end_time=datetime.utcnow() + timedelta(minutes=15),
        ticket=ticket
    )
    db.session.add(reservation)
    db.session.commit()
    return jsonify({
        'token': ticket.token
    })


def get_reservation(event_id, reservation_token) -> Response:
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


def pay_for_reservation(event_id, reservation_token) -> Response:
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


def get_stats() -> Response:
    return jsonify({})


routes = [
    ("/events", get_events, ["GET"]),
    ("/events/<int:event_id>/tickets", get_tickets, ["GET"]),
    ("/stats", get_stats, ["GET"]),
    ("/events/<int:event_id>/reservations/<reservation_token>",
     get_reservation, ["GET"]),
    ("/events/<int:event_id>/reservations", ticket_reservation, ["POST"]),
    ("/events/<int:event_id>/reservations/<reservation_token>/pay",
     pay_for_reservation, ["POST"]),
]


def add_routes(app: Flask):
    for route in routes:
        app.add_url_rule(route[0], view_func=route[1], methods=route[2])
