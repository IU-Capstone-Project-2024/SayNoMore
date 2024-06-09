import requests
import air_api_data


class AirTicketsApi:
    """
    This class interacts with all flight ticket requests
    """

    def __init__(self):
        # Initialize API token and endpoints
        self.api_token = air_api_data.api_token

        # URLs for different API endpoints
        self.fetch_cheapest_tickets_url = air_api_data.fetch_cheapest_tickets_url
        self.fetch_grouped_tickets_url = air_api_data.fetch_grouped_tickets_url
        self.fetch_period_tickets_url = air_api_data.fetch_period_tickets_url
        self.fetch_alternative_route_tickets_url = air_api_data.fetch_alternative_route_tickets_url
        self.fetch_popular_routes_from_city_url = air_api_data.fetch_popular_routes_from_city_url
        self.fetch_airline_logos_url = air_api_data.fetch_airline_logos_url

    def fetch_cheapest_tickets(self, origin, destination=None, currency='rub', departure_at=None, return_at=None,
                               one_way=True, direct=False, market='ru', limit=30, page=1, sorting='price',
                               unique=False):
        """
               Fetch the cheapest air tickets for specific dates.

               :param origin: Departure point (IATA code).
               :param destination: Destination point (IATA code).
               :param currency: Currency of the ticket prices. Default is 'rub'.
               :param departure_at: Departure date (format YYYY-MM or YYYY-MM-DD).
               :param return_at: Return date (format YYYY-MM or YYYY-MM-DD).
               :param one_way: One way ticket. Default is True.
               :param direct: Direct flights only. Default is False.
               :param market: Data source market. Default is 'ru'.
               :param limit: Number of records in the response. Default is 30.
               :param page: Page number to skip the first records. Default is 1.
               :param sorting: Sorting of prices. Default is 'price'. Can be 'price' or 'route'
               :param unique: Return only unique directions if origin is specified but destination is not. Default is False.
               :return: JSON response with the structure:
                    {
                        "success": bool,  # Indicates the success of the request
                        "data": [
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
                            },
                            ...
                        ]
                    }
               """
        params = {
            'currency': currency,
            'origin': origin,
            'destination': destination,
            'departure_at': departure_at,
            'return_at': return_at,
            'one_way': one_way,
            'direct': direct,
            'market': market,
            'limit': limit,
            'page': page,
            'sorting': sorting,
            'unique': unique,
            'token': self.api_token
        }

        # Send a GET request to fetch the cheapest tickets
        response = requests.get(self.fetch_cheapest_tickets_url, params=params)
        return response.json()

    def fetch_grouped_tickets(self, currency='rub', origin=None, destination=None, group_by='departure_at',
                              departure_at=None, return_at=None, market='ru', direct=False, trip_duration=None):
        """
        Fetch grouped cheap air tickets.

        :param currency: Currency of the ticket prices. Default is 'rub'.
        :param origin: Departure point (IATA code).
        :param destination: Destination point (IATA code).
        :param group_by: Group by departure date, return date, or month. Default is 'departure_at'. Can be 'departure_at', 'return_at', 'month'
        :param departure_at: Departure date (format YYYY-MM or YYYY-MM-DD).
        :param return_at: Return date (format YYYY-MM or YYYY-MM-DD).
        :param market: Data source market. Default is 'ru'.
        :param direct: Direct flights only. Default is False.
        :param trip_duration: Duration of the trip.
        :return: JSON response with the structure:
            {
                "success": bool,  # Indicates the success of the request
                "data": {
                    "2021-11-01": [
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
                            "duration": int,  # Duration of the flight in minutes
                            "link": str,  # Link to the ticket on Aviasales
                            "currency": str  # Currency of the ticket price
                        },
                        ...
                    ]
                }
            }
        """
        params = {
            'currency': currency,
            'origin': origin,
            'destination': destination,
            'group_by': group_by,
            'departure_at': departure_at,
            'return_at': return_at,
            'market': market,
            'direct': direct,
            'trip_duration': trip_duration,
            'token': self.api_token
        }

        # Send a GET request to fetch grouped tickets
        response = requests.get(self.fetch_grouped_tickets_url, params=params)
        return response.json()
