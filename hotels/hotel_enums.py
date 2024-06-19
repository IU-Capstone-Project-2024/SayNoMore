from enum import Enum

class Language(Enum):
    EN = 'en'
    RU = 'ru'
    ES = 'es'

class Currency(Enum):
    RUB = 'rub'
    USD = 'usd'
    EUR = 'eur'

class LookFor(Enum):
    CITY = 'city'
    HOTEL = 'hotel'
    BOTH = 'both'

class ConvertCase(Enum):
    ENABLED = 1
    DISABLED = 0

class CollectionType(Enum):
    POPULARITY = 'popularity'
    RATING = 'rating'
    DISTANCE = 'distance'
