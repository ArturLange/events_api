from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class TicketType(Base):
    __tablename__ = 'ticket_types'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    event_id = Column(Integer, ForeignKey('events.id'))
    event = relationship("Event", back_populates="ticket_types")


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

    def to_dict(self):
        return {
            'id': self.id,
            "name": self.name,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "ticket_types": [ticket_type.name for ticket_type in self.ticket_types]
        }
