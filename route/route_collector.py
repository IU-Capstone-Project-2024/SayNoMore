from air_tickets.air_tickets_api import AirTicketsApi
from hotels.hotel_api import HotelApi


class RouteCollector:
    """
    This class creates a route consisting of air tickets and hotels
    """

    def __init__(self):
        self.hotel_api = HotelApi()
        self.air_api = AirTicketsApi()

    def get_ticket(self, origin, destination, departure_at=None, return_at=None, budget=None):
        """
        Fetch the cheapest air ticket based on the specified parameters.

        :param origin: str, IATA code of the departure point
        :param destination: str, IATA code of the destination point
        :param departure_at: str, optional, departure date (format YYYY-MM or YYYY-MM-DD)
        :param return_at: str, optional, return date (format YYYY-MM or YYYY-MM-DD)
        :param budget: float, optional, maximum price of the ticket

        :return: dict, the cheapest ticket that matches the criteria:
            {
                "origin": str,  # Departure point
                         "destination": str,  # Destination point
                         "origin_airport": str,  # IATA code of the departure airport
                         "destination_airport": str,  # IATA code of the destination airport
                         "price": float,  # Ticket price
                         "airline": str,  # IATA code of the airline
                         "flight_number": str,  # Flight number
                         "departure_at": str,  # Departure date
                         "return_at": str,  # Return date
                         "transfers": int,  # Number of transfers on the outbound trip
                         "return_transfers": int,  # Number of transfers on the return trip
                         "duration": int,  # Total duration of the round trip in minutes
                         "duration_to": int,  # Duration of the outbound flight in minutes
                         "duration_back": int,  # Duration of the return flight in minutes
                         "link": str,  # Link to the ticket on Aviasales
                         "currency": str  # Currency of the ticket price
            }
        """
        # Initialize an empty list to store tickets
        tickets = []
        # Loop through the first 9 pages to find tickets
        for page in range(1, 10):
            # Fetch the cheapest tickets for the given parameters
            response = self.air_api.fetch_cheapest_tickets(origin=origin,
                                                           destination=destination,
                                                           departure_at=departure_at,
                                                           return_at=return_at,
                                                           one_way=True,
                                                           page=page)
            # Check if the response was successful
            if not response['success']:
                raise Exception('response was not successful')
            # Break the loop if no new ticket data is received
            if len(response['data']) == 0:
                break
            else:
                # Append the received ticket data to the tickets list
                tickets += response['data']
        # Filter tickets by budget if a budget is specified
        if budget:
            # Initialize the last index of the ticket list to include
            last_index = 1
            # Iterate through the tickets to find those within budget
            for i, ticket in enumerate(tickets):
                if ticket['price'] < budget:
                    last_index = i + 1
                else:
                    break
            # Slice the tickets list to only include tickets within budget
            tickets = tickets[:last_index]
        # Return the last ticket in the filtered list, which should be the cheapest
        return tickets[-1]
