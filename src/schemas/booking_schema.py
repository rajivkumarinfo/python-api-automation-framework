# JSON Schemas for Restful-Booker response contracts. Kept as plain Python dicts (not .json files) so they can be composed/reused
# without extra file I/O, but they are pure JSON Schema (draft-07) underneath.


BOOKING_DATES_SCHEMA = {
    "type": "object",
    "properties": {
        "checkin": {"type": "string", "format": "date"},
        "checkout": {"type": "string", "format": "date"},
    },
    "required": ["checkin", "checkout"],
    "additionalProperties": False,
}

BOOKING_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Booking",
    "type": "object",
    "properties": {
        "firstname": {"type": "string", "minLength": 1},
        "lastname": {"type": "string", "minLength": 1},
        "totalprice": {"type": "number", "minimum": 0},
        "depositpaid": {"type": "boolean"},
        "bookingdates": BOOKING_DATES_SCHEMA,
        "additionalneeds": {"type": "string"},
    },
    "required": [
        "firstname",
        "lastname",
        "totalprice",
        "depositpaid",
        "bookingdates",
    ],
    "additionalProperties": False,
}

CREATE_BOOKING_RESPONSE_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "CreateBookingResponse",
    "type": "object",
    "properties": {
        "bookingid": {"type": "integer"},
        "booking": BOOKING_SCHEMA,
    },
    "required": ["bookingid", "booking"],
    "additionalProperties": False,
}

BOOKING_ID_LIST_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "BookingIdList",
    "type": "array",
    "items": {
        "type": "object",
        "properties": {"bookingid": {"type": "integer"}},
        "required": ["bookingid"],
        "additionalProperties": False,
    },
}

AUTH_TOKEN_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "AuthToken",
    "type": "object",
    "properties": {"token": {"type": "string", "minLength": 1}},
    "required": ["token"],
}
