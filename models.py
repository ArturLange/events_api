from datetime import datetime
from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database import db
from utils import get_reservation_end_time


class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)

    reservation_id = db.Column(db.Integer, db.ForeignKey('reservations.id'))
    reservation = relationship("Reservation", back_populates='payments')


class Reservation(db.Model):
    __tablename__ = 'reservations'
    id = db.Column(db.Integer, primary_key=True)
    end_time = db.Column(db.DateTime, default=get_reservation_end_time)

    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'))
    ticket = relationship("Ticket", back_populates='reservations')

    payments = relationship(
        "Payment",
        order_by=Payment.start_time.desc(),
        back_populates='reservation'
    )


class Ticket(db.Model):
    __tablename__ = 'tickets'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(UUID(as_uuid=True), unique=True, default=uuid4)

    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    event = relationship("Event", back_populates="tickets")

    ticket_type_id = db.Column(db.Integer, db.ForeignKey('ticket_types.id'))
    ticket_type = relationship("TicketType", back_populates="tickets")

    reservations = relationship(
        "Reservation",
        order_by=Reservation.end_time,
        back_populates='ticket'
    )


class TicketType(db.Model):
    __tablename__ = 'ticket_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    event = relationship("Event", back_populates="ticket_types")

    tickets = relationship(
        "Ticket",
        order_by=Ticket.id,
        back_populates="ticket_type"
    )


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)

    ticket_types = relationship(
        "TicketType",
        order_by=TicketType.id,
        back_populates="event"
    )

    tickets = relationship(
        "Ticket",
        order_by=Ticket.id,
        back_populates="event"
    )

    def to_dict(self):
        return {
            'id': self.id,
            "name": self.name,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "ticket_types": [ticket_type.name for ticket_type in self.ticket_types]
        }
