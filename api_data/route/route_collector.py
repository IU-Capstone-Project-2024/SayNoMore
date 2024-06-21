from api_data.air_tickets.air_tickets_api import AirTicketsApi
from api_data.hotels.hotel_api import HotelApi


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
        else:
            return tickets[0] if len(tickets) > 0 else None
        # Return the last ticket in the filtered list, which should be the cheapest
        if len(tickets) > 0:
            return tickets[-1]
        else:
            return None

    def get_hotel(self, location, check_in, check_out, budget=None):
        """
        Fetches the hotel based on the specified parameters.

        Parameters:
        - location: str, Name of the location (can use IATA code).
        - check_in: str, Check-in date (format YYYY-MM-DD).
        - check_out: str, Check-out date (format YYYY-MM-DD).
        - budget: float, optional, Maximum price for the hotel.

        Returns:
        - dict: The hotel that matches the criteria or None if no hotels match:
            {
                'locationId': int,  # ID of the location
                'hotelId': int,  # ID of the hotel
                'priceFrom': float,  # Minimum price for staying at the hotel room
                'priceAvg': float,  # Average price for staying at the hotel room
                'pricePercentile': dict,  # Price distribution by percentages
                'stars': int,  # Number of stars of the hotel
                'hotelName': str,  # Name of the hotel
                'location': dict,  # Information about the hotel location
                'geo': dict,  # Coordinates of the location (city)
                'name': str,  # Name of the location (city)
                'state': str,  # State where the city is located
                'country': str  # Country of the hotel
            }
        """

        # Fetch hotel prices based on the provided location, check-in and check-out dates, and limit
        hotels = self.hotel_api.fetch_hotel_prices(location=location,
                                                   check_in=check_in,
                                                   check_out=check_out,
                                                   limit=1000)

        # Sort the fetched hotels by the 'priceFrom' field in ascending order
        hotels = sorted(hotels, key=lambda x: x['priceFrom'])

        # If a budget is specified, filter hotels to include only those with 'priceFrom' less than the budget
        if budget:
            hotels = [hotel for hotel in hotels if hotel['priceFrom'] < budget]
        else:
            return hotels[0] if len(hotels) > 0 else None

        # Return the last hotel in the filtered list (the cheapest within budget), or None if no hotels match
        if len(hotels) > 0:
            return hotels[-1]
        else:
            return None

    def find_top_routes(self, origin, destination, departure_at=None, return_at=None, budget=None, route_number=3):
        """
        Find the top routes based on the cheapest tickets and hotels.

        Parameters:
        - origin: str, IATA code of the departure point.
        - destination: str, IATA code of the destination point.
        - departure_at: str, optional, departure date (format YYYY-MM-DD).
        - return_at: str, optional, return date (format YYYY-MM-DD).
        - budget: float, optional, maximum combined price for the ticket and hotel.
        - route_number: int, optional, number of top routes to find (default is 3).

        Returns:
        - list of dicts: Each dictionary contains a 'ticket' and 'hotel' key with details of the route.
            [{
                'ticket': {
                    'origin': str,
                    'destination': str,
                    'origin_airport': str,
                    'destination_airport': str,
                    'price': float,
                    'airline': str,
                    'flight_number': str,
                    'departure_at': str,
                    'return_at': str,
                    'transfers': int,
                    'return_transfers': int,
                    'duration': int,
                    'duration_to': int,
                    'duration_back': int,
                    'link': str,
                    'currency': str
                },
                'hotel': {
                    'locationId': int,
                    'hotelId': int,
                    'priceFrom': float,
                    'priceAvg': float,
                    'pricePercentile': dict,
                    'stars': int,
                    'hotelName': str,
                    'location': dict,
                    'geo': dict,
                    'name': str,
                    'state': str,
                    'country': str
                }
            }]
        """
        # Get the cheapest ticket and hotel
        cheapest_ticket = self.get_ticket(origin=origin, destination=destination, departure_at=departure_at,
                                          return_at=return_at)
        cheapest_hotel = self.get_hotel(location=origin, check_in=departure_at, check_out=return_at)

        # Create a return array with the initial cheapest route
        top_routes = [{
            'ticket': cheapest_ticket,
            'hotel': cheapest_hotel
        }]

        # Define minimum prices
        min_ticket_price = cheapest_ticket['price']
        min_hotel_price = cheapest_hotel['priceFrom']

        # Check if budget is specified
        if budget:
            # Check if the cheapest route exceeds the budget
            if cheapest_hotel['priceFrom'] + cheapest_ticket['price'] > budget:
                return top_routes
            else:
                # Make return value empty
                top_routes = []
                # Define part of a budget for tickets and hotels
                coef = min_ticket_price / (min_ticket_price + min_hotel_price)
                ticket_price = max(coef * budget * 0.9, min_ticket_price)
                hotel_price = max((1 - coef) * budget * 0.9, min_hotel_price)

                # Find some routes within the budget
                for _ in range(route_number):
                    ticket = self.get_ticket(origin=origin, destination=destination, departure_at=departure_at,
                                             return_at=return_at, budget=ticket_price)
                    hotel = self.get_hotel(location=origin, check_in=departure_at, check_out=return_at,
                                           budget=hotel_price)
                    top_routes.append({
                        'ticket': ticket,
                        'hotel': hotel
                    })
                    ticket_price *= 1.1
                    hotel_price *= 1.1
        else:
            # Budget is not specified, finding arbitrary routes
            for _ in range(1, route_number):
                min_ticket_price *= 2
                ticket = self.get_ticket(origin=origin, destination=destination, departure_at=departure_at,
                                         return_at=return_at, budget=min_ticket_price)
                min_hotel_price *= 3
                hotel = self.get_hotel(location=origin, check_in=departure_at, check_out=return_at,
                                       budget=min_hotel_price)
                top_routes.append({
                    'ticket': ticket,
                    'hotel': hotel
                })

        # Remove duplicates
        unique_routes = []
        for i in range(len(top_routes)):
            if i == 0 or (top_routes[i]['ticket'] != top_routes[i - 1]['ticket'] and top_routes[i]['hotel'] !=
                          top_routes[i - 1]['hotel']):
                unique_routes.append(top_routes[i])

        return unique_routes
