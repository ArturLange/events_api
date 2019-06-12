from datetime import datetime, timedelta


def get_reservation_end_time(duration: int = 15):
    return datetime.now() + timedelta(minutes=duration)
