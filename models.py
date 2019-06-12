from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database import Base
from utils import get_reservation_end_time


class Reservation(Base):
    __tablename__ = 'reservations'
    id = Column(Integer, primary_key=True)
    end_time = Column(DateTime, default=get_reservation_end_time)

    ticket_id = Column(Integer, ForeignKey('tickets.id'))
    ticket = relationship("Ticket", back_populates='reservations')


class Ticket(Base):
    __tablename__ = 'tickets'
    id = Column(Integer, primary_key=True)
    token = Column(UUID(as_uuid=True), unique=True, default=uuid4)

    event_id = Column(Integer, ForeignKey('events.id'))
    event = relationship("Event", back_populates="tickets")

    ticket_type_id = Column(Integer, ForeignKey('ticket_types.id'))
    ticket_type = relationship("TicketType", back_populates="tickets")

    reservations = relationship(
        "Reservation",
        order_by=Reservation.end_time,
        back_populates='ticket'
    )


class TicketType(Base):
    __tablename__ = 'ticket_types'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    event_id = Column(Integer, ForeignKey('events.id'))
    event = relationship("Event", back_populates="ticket_types")

    tickets = relationship(
        "Ticket",
        order_by=Ticket.id,
        back_populates="ticket_type"
    )


class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)

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
