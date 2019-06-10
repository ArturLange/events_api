from datetime import datetime

from database import db_session, init_db
from models import Event


def add_events():
    event1 = Event(
        name="Woodstock Festival",
        start_time=datetime(1999, 7, 23, 12),
        end_time=datetime(1999, 7, 25, 12),
    )
    event2 = Event(
        name="Cirque du Soleil",
        start_time=datetime(2019, 10, 23, 20, 0),
        end_time=datetime(2019, 10, 23, 23, 0),
    )
    db_session.add(event1)
    db_session.add(event2)
    db_session.commit()


if __name__ == "__main__":
    init_db()
    add_events()
