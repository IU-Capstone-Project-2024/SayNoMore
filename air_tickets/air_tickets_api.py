import requests
from air_tickets import air_api_data


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

    def fetch_cheapest_tickets(self, origin=None, destination=None, currency='rub', departure_at=None, return_at=None,
                               one_way='true', direct='false', market='ru', limit=30, page=1, sorting='price',
                               unique='false'):
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

        try:
            # Send a GET request to fetch the cheapest tickets
            response = requests.get(self.fetch_cheapest_tickets_url, params=params)
            # Check if the request was successful
            if response.status_code != 200:
                # Raise an exception if the response status code indicates failure
                raise Exception(f"Failed to fetch cheapest tickets. Status code: {response.status_code}")
            # Return the JSON content of the response
            return response.json()

        except requests.exceptions.RequestException as e:
            # Catch any request-related exceptions (e.g., timeouts, connection errors)
            raise Exception("There was an error making the request.") from e

    def fetch_grouped_tickets(self, currency='rub', origin=None, destination=None, group_by='departure_at',
                              departure_at=None, return_at=None, market='ru', direct='false', trip_duration=None):
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

        try:
            # Send a GET request to fetch grouped tickets
            response = requests.get(self.fetch_grouped_tickets_url, params=params)
            # Check if the request was successful
            if response.status_code != 200:
                # Raise an exception if the response status code indicates failure
                raise Exception(f"Failed to fetch cheapest tickets. Status code: {response.status_code}")
            # Return the JSON content of the response
            return response.json()

        except requests.exceptions.RequestException as e:
            # Catch any request-related exceptions (e.g., timeouts, connection errors)
            raise Exception("There was an error making the request.") from e

    def fetch_period_tickets(self, currency='rub', origin='MOW', destination=None, beginning_of_period=None,
                             period_type=None, group_by='dates', one_way='true', page=1, market='ru', limit=30,
                             sorting='price', trip_duration=None, trip_class=0):
        """
        Fetch air ticket prices for a specified period.

        :param currency: Currency of the ticket prices. Default is 'rub'.
        :param origin: Departure point (IATA code of country, city, or airport). Default is 'MOW'.
        :param destination: Destination point (IATA code of country, city, or airport).
        :param beginning_of_period: Start of the period for departure date.
        :param period_type: Period type (year, month, or day). If not specified, defaults to tickets for the current month.
        :param group_by: Grouping parameter (dates or directions). Default is 'dates'.
        :param one_way: One way ticket. Default is True.
        :param page: Page number for pagination. Default is 1.
        :param market: Data source market. Default is 'ru'.
        :param limit: Number of records per page. Default is 30.
        :param sorting: Sorting of prices (price, route, or distance_unit_price). Default is 'price'.
        :param trip_duration: Duration of the trip in days.
        :param trip_class: Class of service (0 for economy, 1 for business, 2 for first class). Default is 0.
        :return: JSON response with the structure:
            {
                "success": bool,  # Indicates the success of the request
                "data": [
                    {
                        "origin": str,  # Departure point
                        "destination": str,  # Destination point
                        "depart_date": str,  # Departure date
                        "distance": int,  # Flight distance in kilometers
                        "duration": int,  # Flight duration in minutes
                        "return_date": str,  # Return date
                        "number_of_changes": int,  # Number of changes (layovers)
                        "value": float,  # Flight cost in the specified currency
                        "found_at": str,  # Time and date when the ticket was found
                        "trip_class": int  # Class of service (0 for economy, 1 for business, 2 for first class)
                    },
                    ...
                ]
            }
        """
        params = {
            'currency': currency,
            'origin': origin,
            'destination': destination,
            'beginning_of_period': beginning_of_period,
            'period_type': period_type,
            'group_by': group_by,
            'one_way': one_way,
            'page': page,
            'market': market,
            'limit': limit,
            'sorting': sorting,
            'trip_duration': trip_duration,
            'trip_class': trip_class,
            'token': self.api_token
        }

        try:
            # Send a GET request to fetch period tickets
            response = requests.get(self.fetch_period_tickets_url, params=params)
            # Check if the request was successful
            if response.status_code != 200:
                # Raise an exception if the response status code indicates failure
                raise Exception(f"Failed to fetch cheapest tickets. Status code: {response.status_code}")
            # Return the JSON content of the response
            return response.json()

        except requests.exceptions.RequestException as e:
            # Catch any request-related exceptions (e.g., timeouts, connection errors)
            raise Exception("There was an error making the request.") from e

    def fetch_alternative_route_tickets(self, currency='rub', origin=None, destination=None, show_to_affiliates='false',
                                        depart_date=None, return_date=None, distance=None, market='ru', limit=1,
                                        flexibility=0):
        """
        Fetch alternative route tickets based on the given parameters.

        :param currency: Currency of the ticket prices. Default is 'rub'.
        :param origin: Origin point (IATA code or country code). Length should be between 2 and 3 characters.
        :param destination: Destination point (IATA code or country code). Length should be between 2 and 3 characters.
        :param show_to_affiliates: Show prices found with partner markers. Default is False.
        :param depart_date: Departure date in 'YYYY-MM-DD' format.
        :param return_date: Return date in 'YYYY-MM-DD' format.
        :param distance: Distance in kilometers from origin and destination points where they search for nearby cities.
        :param market: Data source market. Default is 'ru'.
        :param limit: Number of output options from 1 to 20. Default is 1.
        :param flexibility: Range extension around the specified dates. Value can be from 0 to 7.
        :return: JSON response with the following structure:
            {
                "success": bool,  # Indicates whether the request was successful
                "data": [
                    {
                        "origin": str,  # The origin point (city or country code)
                        "destination": str,  # The destination point (city or country code)
                        "depart_date": str,  # The departure date in 'YYYY-MM-DD' format
                        "distance": int,  # The total flight distance in kilometers
                        "duration": int,  # The total flight duration in minutes, including layovers
                        "return_date": str,  # The return date in 'YYYY-MM-DD' format
                        "number_of_changes": int,  # The number of layovers or changes in the itinerary
                        "value": float,  # The cost of the flight in the specified currency
                        "found_at": str,  # The time and date when the ticket was found
                        "trip_class": int  # The class of service for the flight (0 for economy, 1 for business, 2 for first class)
                    },
                   ...
                ]
            }
        """
        params = {
            'currency': currency,
            'origin': origin,
            'destination': destination,
            'show_to_affiliates': show_to_affiliates,
            'depart_date': depart_date,
            'return_date': return_date,
            'distance': distance,
            'market': market,
            'limit': limit,
            'flexibility': flexibility,
            'token': self.api_token
        }

        try:
            # Send a GET request to fetch alternative route tickets
            response = requests.get(self.fetch_alternative_route_tickets_url, params=params)
            # Check if the request was successful
            if response.status_code != 200:
                # Raise an exception if the response status code indicates failure
                raise Exception(f"Failed to fetch cheapest tickets. Status code: {response.status_code}")
            # Return the JSON content of the response
            return response.json()

        except requests.exceptions.RequestException as e:
            # Catch any request-related exceptions (e.g., timeouts, connection errors)
            raise Exception("There was an error making the request.") from e

    def fetch_popular_routes_from_city(self, origin=None, currency='rub'):
        """
        Fetch popular routes from a city based on the given parameters.

        :param origin: Origin point (IATA code of the city).
        :param currency: Currency of the ticket prices. Default is 'rub'.
        :return: JSON response with the following structure:
            {
                "success": bool,  # Indicates the result of the request
                "data": {
                    "AER": {  # Example key for a destination; actual keys depend on available routes
                        "origin": str,  # The origin point (IATA code of the city)
                        "destination": str,  # The destination point (IATA code of the city)
                        "departure_at": str,  # The departure date and time in 'YYYY-MM-DDTHH:MM:SSZ' format
                        "return_at": str,  # The return date and time in 'YYYY-MM-DDTHH:MM:SSZ' format
                        "number_of_changes": int,  # The number of layovers or changes in the itinerary
                        "price": float,  # The cost of the flight in the specified currency
                        "found_at": str,  # The time and date when the ticket was found
                        "transfers": int,  # The number of layovers
                        "airline": str,  # The IATA code of the airline
                        "flight_number": int,  # The flight number
                        "currency": str  # The currency used for pricing information
                    },
                  ...  # Additional routes may be included depending on the query results
                },
                "error": null,  # Any error messages returned by the API
                "currency": str  # The currency used for pricing information
            }
        """
        params = {
            'origin': origin,
            'currency': currency,
            'token': self.api_token
        }

        try:
            # Send a GET request to fetch popular routes from the city
            response = requests.get(self.fetch_popular_routes_from_city_url, params=params)
            # Check if the request was successful
            if response.status_code != 200:
                # Raise an exception if the response status code indicates failure
                raise Exception(f"Failed to fetch cheapest tickets. Status code: {response.status_code}")
            # Return the JSON content of the response
            return response.json()

        except requests.exceptions.RequestException as e:
            # Catch any request-related exceptions (e.g., timeouts, connection errors)
            raise Exception("There was an error making the request.") from e