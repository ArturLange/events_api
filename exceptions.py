import json

from flask import Response
from werkzeug.exceptions import HTTPException, NotFound


class JSONException(HTTPException):
    def __init__(self, error: str, status_code: int):
        return super().__init__(response=Response(
            json.dumps({'error': error}),
            status_code,
            content_type='application/json'
        ))


class EventNotFound(JSONException):
    def __init__(self):
        return super().__init__(
            error='Event not found',
            status_code=404
        )


class NoTicketTypeFound(JSONException):
    def __init__(self):
        return super().__init__(
            error='Event has no tickets of given type',
            status_code=404
        )


class NoTicketsAvailable(JSONException):
    def __init__(self):
        return super().__init__(
            error='No tickets available',
            status_code=404
        )


class TicketNotFound(JSONException):
    def __init__(self):
        return super().__init__(
            error='Ticket not found',
            status_code=404
        )


class EventIDNotGiven(JSONException):
    def __init__(self):
        return super().__init__(
            error="'event_id' parameter not given",
            status_code=400
        )
