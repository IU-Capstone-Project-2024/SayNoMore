import requests
from api_collector.air_tickets import air_api_data
import os
from api_collector.air_tickets.flight_enums import Currency, Market, Sorting, GroupBy, PeriodType, TripClass


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
        self.fetch_airline_logos_url_base = air_api_data.fetch_airline_logos_url_base
        self.air_logo_dir = "/photos/airline_logos"

    def data_directory_path(self):
        """
        This function determine absolute path to data directory
        :return: absolute path to data directory
        """
        # Get the absolute path of the current script
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Find the project root directory (assuming this script is inside SayNoMore or its subdirectories)
        project_root = current_dir
        while os.path.basename(project_root) != 'SayNoMore':
            project_root = os.path.dirname(project_root)

        # Construct the path to the data directory
        data_directory = os.path.join(project_root, 'data')

        # Ensure the data directory exists
        os.makedirs(data_directory, exist_ok=True)

        return data_directory

    def fetch_cheapest_tickets(self,
                               currency=Currency.RUB,
                               origin=None,
                               destination=None,
                               departure_at=None,
                               return_at=None,
                               one_way=True,
                               direct=False,
                               market=Market.RU,
                               limit=30,
                               page=1,
                               sorting=Sorting.PRICE,
                               unique=False):
        """
        Fetch the cheapest air tickets for specific dates.

        :param currency: Currency of the ticket prices. Default is 'rub'.
        :param origin: Departure point (IATA code).
        :param destination: Destination point (IATA code).
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
            'currency': currency.value,
            'origin': origin,
            'destination': destination,
            'departure_at': departure_at,
            'return_at': return_at,
            'one_way': str(one_way).lower(),
            'direct': str(direct).lower(),
            'market': market.value,
            'limit': limit,
            'page': page,
            'sorting': sorting.value,
            'unique': str(unique).lower(),
            'token': self.api_token
        }

        try:
            # Send a GET request to fetch the cheapest tickets
            response = requests.get(self.fetch_cheapest_tickets_url,
                                    params=params)
            # Check if the request was successful
            if response.status_code != 200:
                # Raise an exception if the response status code indicates failure
                raise Exception(
                    f"Failed to fetch cheapest tickets. Status code: {response.status_code}"
                )
            # Return the JSON content of the response
            return response.json()

        except requests.exceptions.RequestException as e:
            # Catch any request-related exceptions (e.g., timeouts, connection errors)
            raise Exception("There was an error making the request.") from e

    def fetch_grouped_tickets(self,
                              currency=Currency.RUB,
                              origin=None,
                              destination=None,
                              group_by=GroupBy.DEPARTURE_AT,
                              departure_at=None,
                              return_at=None,
                              market=Market.RU,
                              direct=False,
                              trip_duration=None):
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
            'currency': currency.value,
            'origin': origin,
            'destination': destination,
            'group_by': group_by.value,
            'departure_at': departure_at,
            'return_at': return_at,
            'market': market.value,
            'direct': str(direct).lower(),
            'trip_duration': trip_duration,
            'token': self.api_token
        }

        try:
            # Send a GET request to fetch grouped tickets
            response = requests.get(self.fetch_grouped_tickets_url,
                                    params=params)
            # Check if the request was successful
            if response.status_code != 200:
                # Raise an exception if the response status code indicates failure
                raise Exception(
                    f"Failed to fetch cheapest tickets. Status code: {response.status_code}"
                )
            # Return the JSON content of the response
            return response.json()

        except requests.exceptions.RequestException as e:
            # Catch any request-related exceptions (e.g., timeouts, connection errors)
            raise Exception("There was an error making the request.") from e

    def fetch_period_tickets(self,
                             currency=Currency.RUB,
                             origin='MOW',
                             destination=None,
                             beginning_of_period=None,
                             period_type=PeriodType.MONTH,
                             group_by=GroupBy.DATES,
                             one_way=True,
                             page=1,
                             market=Market.RU,
                             limit=30,
                             sorting=Sorting.PRICE,
                             trip_duration=None,
                             trip_class=TripClass.ECONOMY):
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
            'currency': currency.value,
            'origin': origin,
            'destination': destination,
            'beginning_of_period': beginning_of_period,
            'period_type': period_type.value,
            'group_by': group_by.value,
            'one_way': str(one_way).lower(),
            'page': page,
            'market': market.value,
            'limit': limit,
            'sorting': sorting.value,
            'trip_duration': trip_duration,
            'trip_class': trip_class.value,
            'token': self.api_token
        }

        try:
            # Send a GET request to fetch period tickets
            response = requests.get(self.fetch_period_tickets_url,
                                    params=params)
            # Check if the request was successful
            if response.status_code != 200:
                # Raise an exception if the response status code indicates failure
                raise Exception(
                    f"Failed to fetch period tickets. Status code: {response.status_code}"
                )
            # Return the JSON content of the response
            return response.json()

        except requests.exceptions.RequestException as e:
            # Catch any request-related exceptions (e.g., timeouts, connection errors)
            raise Exception("There was an error making the request.") from e

    def fetch_alternative_route_tickets(self,
                                        currency=Currency.RUB,
                                        origin=None,
                                        destination=None,
                                        show_to_affiliates=False,
                                        depart_date=None,
                                        return_date=None,
                                        distance=None,
                                        market=Market.RU,
                                        limit=1,
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
            'currency': currency.value,
            'origin': origin,
            'destination': destination,
            'show_to_affiliates': str(show_to_affiliates).lower(),
            'depart_date': depart_date,
            'return_date': return_date,
            'distance': distance,
            'market': market.value,
            'limit': limit,
            'flexibility': flexibility,
            'token': self.api_token
        }

        try:
            # Send a GET request to fetch alternative route tickets
            response = requests.get(self.fetch_alternative_route_tickets_url,
                                    params=params)
            # Check if the request was successful
            if response.status_code != 200:
                # Raise an exception if the response status code indicates failure
                raise Exception(
                    f"Failed to fetch alternative route tickets. Status code: {response.status_code}"
                )
            # Return the JSON content of the response
            return response.json()

        except requests.exceptions.RequestException as e:
            # Catch any request-related exceptions (e.g., timeouts, connection errors)
            raise Exception("There was an error making the request.") from e

    def fetch_popular_routes_from_city(self,
                                       origin=None,
                                       currency=Currency.RUB):
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
            'currency': currency.value,
            'token': self.api_token
        }

        try:
            # Send a GET request to fetch popular routes from the city
            response = requests.get(self.fetch_popular_routes_from_city_url,
                                    params=params)
            # Check if the request was successful
            if response.status_code != 200:
                # Raise an exception if the response status code indicates failure
                raise Exception(
                    f"Failed to fetch popular routes. Status code: {response.status_code}"
                )
            # Return the JSON content of the response
            return response.json()

        except requests.exceptions.RequestException as e:
            # Catch any request-related exceptions (e.g., timeouts, connection errors)
            raise Exception("There was an error making the request.") from e

    def fetch_airline_logo(self, iata_code, height=100, width=100):
        """
        Fetches the logo for a single airline based on its IATA code and saves it as a.png file
        Airline logo is saved to /data/photos/airline_logos/<iata_code>.png

        :param iata_code: IATA code of the airline whose logo needs to be fetched.
        :param height: Desired height of the logo in pixels.
        :param width: Desired width of the logo in pixels.
        :return: None
        """

        logo_directory = self.data_directory_path() + self.air_logo_dir
        os.makedirs(logo_directory,
                    exist_ok=True)  # Ensure the directory exists

        # Construct the URL for the airline logo using the base URL, IATA code, and dimensions
        logo_url = f"{self.fetch_airline_logos_url_base}{width}/{height}/{iata_code}.png"
        # Define the local path for saving the logo
        logo_path = os.path.join(logo_directory, f"{iata_code}.png")

        # Attempt to fetch the logo
        try:
            response = requests.get(logo_url)
            # If the request is successful, save the logo to the local directory
            if response.status_code == 200:
                with open(logo_path, 'wb') as file:
                    file.write(response.content)
            else:
                raise Exception(
                    f"Failed to fetch cheapest tickets. Status code: {response.status_code}"
                )
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch logo for {iata_code}: {str(e)}")
