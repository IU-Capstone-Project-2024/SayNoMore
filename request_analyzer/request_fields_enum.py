from enum import Enum


class RequestField(Enum):
    Arrival = ("Arrival", True)
    Return = ("Return", True)
    Departure = ("Departure", True)
    Destination = ("Destination", True)
    Budget = ("Budget", False)

    def __init__(self, value, is_required):
        self._value_ = value
        self.is_required = is_required

    @property
    def value(self):
        return self._value_
