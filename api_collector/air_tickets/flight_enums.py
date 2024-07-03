from enum import Enum


class Currency(Enum):
    RUB = 'rub'
    USD = 'usd'
    EUR = 'eur'


class Market(Enum):
    RU = 'ru'
    US = 'us'
    EU = 'eu'


class Sorting(Enum):
    PRICE = 'price'
    ROUTE = 'route'
    DISTANCE_UNIT_PRICE = 'distance_unit_price'


class GroupBy(Enum):
    DEPARTURE_AT = 'departure_at'
    RETURN_AT = 'return_at'
    MONTH = 'month'
    DATES = 'dates'
    DIRECTIONS = 'directions'


class TripClass(Enum):
    ECONOMY = 0
    BUSINESS = 1
    FIRST_CLASS = 2


class PeriodType(Enum):
    YEAR = 'year'
    MONTH = 'month'
    DAY = 'day'
