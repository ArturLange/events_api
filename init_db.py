from datetime import datetime

from database import db_session, init_db
from models import Event, Ticket, TicketType


def add_events():
    """ Create sample events data
    """

    ### ADD EVENT 1 ###
    event1 = Event(
        name="Woodstock Festival",
        start_time=datetime(1999, 7, 23, 12),
        end_time=datetime(1999, 7, 25, 12),
    )
    premium = TicketType(name='Premium')
    regular = TicketType(name='Regular')
    event1.ticket_types.append(premium)
    event1.ticket_types.append(regular)

    for i in range(120):
        ticket = Ticket()
        event1.tickets.append(ticket)
        premium.tickets.append(ticket)

    for i in range(250):
        ticket = Ticket()
        event1.tickets.append(ticket)
        regular.tickets.append(ticket)

    ### ADD EVENT 2 ###

    event2 = Event(
        name="Cirque du Soleil",
        start_time=datetime(2019, 10, 23, 20, 0),
        end_time=datetime(2019, 10, 23, 23, 0),
    )
    event2.ticket_types.append(TicketType(name='Premium'))
    event2.ticket_types.append(TicketType(name='Regular'))
    event2.ticket_types.append(TicketType(name='VIP'))

    premium = TicketType(name='Premium')
    regular = TicketType(name='Regular')
    vip = TicketType(name='VIP')

    for i in range(50):
        ticket = Ticket()
        event2.tickets.append(ticket)
        premium.tickets.append(ticket)

    for i in range(120):
        ticket = Ticket()
        event2.tickets.append(ticket)
        regular.tickets.append(ticket)

    for i in range(10):
        ticket = Ticket()
        event2.tickets.append(ticket)
        vip.tickets.append(ticket)

    db_session.add(event1)
    db_session.add(event2)
    db_session.commit()


if __name__ == "__main__":
    init_db()
    add_events()
