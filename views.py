import json
from datetime import datetime, timedelta
from exceptions import (
    EventIDNotGiven,
    EventNotFound,
    NoTicketsAvailable,
    NoTicketTypeFound,
    TicketNotFound
)

from flask import Flask, Response, abort, jsonify, request
from sqlalchemy.orm.query import Query
from sqlalchemy.sql.expression import literal

from database import db
from models import Event, Payment, Reservation, Ticket, TicketType
from payment_gateway import (
    CardError,
    CurrencyError,
    PaymentError,
    PaymentGateway
)


def get_available_tickets(ticket_type_id: int) -> Query:
    return db.session.query(Ticket).filter_by(
        ticket_type_id=ticket_type_id).filter(~Ticket.reservations.any(Reservation.end_time > datetime.utcnow()))


def get_events() -> Response:
    events = [event.to_dict() for event in Event.query.all()]
    return jsonify(events)


def get_tickets(event_id) -> Response:
    event_exists = db.session.query(Event).filter_by(id=event_id).count() > 0
    if not event_exists:
        raise EventNotFound()
    ticket_types = db.session.query(
        TicketType).filter_by(event_id=event_id).filter(TicketType.tickets.any()).all()
    response = {
        ticket_type.name: get_available_tickets(ticket_type.id).count()
        for ticket_type in ticket_types
    }
    return jsonify(response)


def ticket_reservation(event_id) -> Response:
    event_exists = db.session.query(Event).filter_by(id=event_id).count() > 0
    if not event_exists:
        raise EventNotFound()
    ticket_type_id = db.session.query(TicketType.id).filter_by(
        event_id=event_id).filter_by(name=request.json['ticket_type']).first()
    if not ticket_type_id:
        raise NoTicketTypeFound()
    ticket = get_available_tickets(ticket_type_id[0]).first()
    if not ticket:
        raise NoTicketsAvailable()
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
    ticket = db.session.query(Ticket).filter_by(
        token=reservation_token).first()
    if not ticket:
        raise TicketNotFound()
    reservation = db.session.query(Reservation).filter_by(
        ticket=ticket).first()
    is_paid = db.session.query(Payment).filter_by(
        reservation=reservation).filter_by(completed=True).count() > 0
    response = {
        'paid': is_paid,
        "event": ticket.event.to_dict(),
        "ticket_type": ticket.ticket_type.name
    }
    return jsonify(response)


def pay_for_reservation(event_id, reservation_token) -> Response:
    payment_token = request.json['payment_token']
    ticket = db.session.query(Ticket).filter_by(
        token=reservation_token).first()
    reservation = ticket.reservations[0]
    payment = Payment(reservation=reservation)

    try:
        payment_result = PaymentGateway().charge(100, payment_token)
        payment.completed = True
    except (CardError, PaymentError, CurrencyError):
        pass
    db.session.add(payment)
    db.session.commit()
    return jsonify({
        "paid": payment.completed,
        "event": ticket.event.to_dict(),
        "ticket_type": ticket.ticket_type.name
    })


def get_stats() -> Response:
    event_id = request.args.get('event_id')
    ticket_type_name = request.args.get('ticket_type')
    tickets = db.session.query(Ticket)
    if event_id:
        if ticket_type_name:
            ticket_type = db.session.query(
                TicketType).filter_by(event_id=event_id).filter_by(name=ticket_type_name).first()
            tickets = tickets.filter_by(ticket_type=ticket_type)
            response = {
                'tickets_available': tickets.filter(~Ticket.reservations.any(Reservation.end_time > datetime.utcnow())).count(),
                'tickets_all': tickets.count()
            }
        else:
            ticket_types = db.session.query(
                TicketType).filter_by(event_id=event_id).all()
            response = {
                ticket_type.name: {
                    'tickets_available': tickets.filter_by(
                        ticket_type=ticket_type).filter(~Ticket.reservations.any(Reservation.end_time > datetime.utcnow())).count(),
                    'tickets_all': tickets.filter_by(
                        ticket_type=ticket_type).count()
                }
                for ticket_type in ticket_types
            }

    else:
        raise EventIDNotGiven()
    return jsonify(response)


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
