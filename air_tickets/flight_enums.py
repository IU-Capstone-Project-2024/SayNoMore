from enum import Enum

class Currency(Enum):
    RUB = 'rub'
    USD = 'usd'
    EUR = 'eur'
    # Add other currencies as needed

class Market(Enum):
    RU = 'ru'
    US = 'us'
    EU = 'eu'
    # Add other markets as needed

class Sorting(Enum):
    PRICE = 'price'
    ROUTE = 'route'