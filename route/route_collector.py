from air_tickets.air_tickets_api import AirTicketsApi
from hotels.hotel_api import HotelApi

class RouteCollector:
    """
    This class creates a route consisting of air tickets and hotels
    """
    def __init__(self):
        self.hotel_api = HotelApi()
        self.air_api = AirTicketsApi()

    def get_tickets(self, origin, destination, departure_at=None, return_at=None):
        response = self.air_api.fetch_cheapest_tickets()
