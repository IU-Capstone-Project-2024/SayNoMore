import requests
from hotels import hotel_api_data
import os


class HotelApi:
    """
    This class with all hotel requests
    """

    def __init__(self):
        self.api_token = hotel_api_data.api_token

        self.search_hotel_or_location_url = hotel_api_data.search_hotel_or_location_url
        self.fetch_hotel_prices_url = hotel_api_data.fetch_hotel_prices_url
        self.fetch_hotel_collections_url = hotel_api_data.fetch_hotel_collections_url
        self.fetch_hotel_collection_types_url = hotel_api_data.fetch_hotel_collection_types_url
        self.fetch_room_types_url = hotel_api_data.fetch_room_types_url
        self.fetch_hotel_types_url = hotel_api_data.fetch_hotel_types_url
        self.fetch_hotel_photos_base_url = hotel_api_data.fetch_hotel_photos_base_url

    def search_hotel_or_location(self, query, lang='en', lookFor='both', limit=10, convertCase=1):
        """
        Searches for hotels or locations based on the provided query.

        Parameters:
        - query: The main parameter that can be text, IATA city code, or latitude/longitude coordinates.
        - lang: Language code for the output. Defaults to 'en'.
        - lookFor: What objects to display in results ('city', 'hotel', 'both'). Defaults to 'both'.
        - limit: Limit on the number of results to display (1-10). Defaults to 10.
        - convertCase: Automatic keyboard layout change flag (1 or 0). Defaults to 1.

        Returns:
            A dictionary containing the search results. The structure includes:
            - 'locations': A list of location objects. Each object contains:
                - 'cityName': Name of the city.
                - 'fullName': Full name of the city and its country.
                - 'countryCode': Country code.
                - 'countryName': Name of the country.
                - 'iata': IATA airport codes for airports in the city, may include multiple codes.
                - 'id': ID of the location in the database.
                - 'hotelsCount': Number of hotels in the location.
                - 'location': Geographical coordinates of the location.
                    - 'lat': Latitude.
                    - 'lon': Longitude.
                - '_score': Internal parameter used for sorting.
            - 'hotels': A list of hotel objects. Each object contains:
                - 'label': Name of the hotel.
                - 'locationName': Location of the hotel.
                - 'locationId': ID of the location where the hotel is located.
                - 'id': ID of the hotel in the database.
                - 'fullName': Full name of the hotel with its location.
                - 'location': Geographical coordinates of the hotel.
                    - 'lat': Latitude.
                    - 'lon': Longitude.
        """
        # Constructing the query string
        params = {
            'query': query,
            'lang': lang,
            'lookFor': lookFor,
            'limit': limit,
            'convertCase': convertCase,
            'token': self.api_token
        }

        try:
            # Making the GET request
            response = requests.get(self.search_hotel_or_location_url, params=params)
            # Check if the request was successful
            if response.status_code != 200:
                # Raise an exception if the response status code indicates failure
                raise Exception(f"Failed to fetch cheapest tickets. Status code: {response.status_code}")
            # Return the JSON content of the response
            return response.json()

        except requests.exceptions.RequestException as e:
            # Catch any request-related exceptions (e.g., timeouts, connection errors)
            raise Exception("There was an error making the request.") from e

    def fetch_hotel_prices(self, location, checkIn, checkOut, locationId=None, hotelId=None, hotel=None,
                           adults=2, limit=4, customerIp=None, currency='USD'):
        """
        Fetches hotel prices based on the provided parameters.

        Parameters:
        - location: Name of the location (can use IATA code).
        - checkIn: Check-in date.
        - checkOut: Check-out date.
        - locationId: ID of the location (can be used instead of location).
        - hotelId: ID of the hotel.
        - hotel: Name of the hotel (must specify location or locationId when using this).
        - adults: Number of guests (default is 2).
        - limit: Number of hotels to return. Default is 4.
        - customerIp: IP address of the user for non-direct requests through server proxy.
        - currency: Currency of the response.
        - token: Your partner token.

        Returns:
            A dictionary containing the hotel price information. The structure includes:
            - 'stars': Number of stars.
            - 'locationId': ID of the location of the hotel.
            - 'priceFrom': Minimum price for staying at the hotel room during the specified period.
            - 'priceAvg': Average price for staying at the hotel room during the specified period.
            - 'pricePercentile': Price distribution by percentages.
            - 'hotelName': Name of the hotel.
            - 'location': Information about the hotel location.
                - 'geo': Coordinates of the location (city).
                - 'name': Name of the location (city).
                - 'state': State where the city is located.
                - 'country': Country of the hotel.
            - 'hotelId': ID of the hotel.
        """
        # Constructing the query string
        params = {
            'location': location,
            'checkIn': checkIn,
            'checkOut': checkOut,
            'locationId': locationId,
            'hotelId': hotelId,
            'hotel': hotel,
            'adults': adults,
            'limit': limit,
            'customerIp': customerIp,
            'currency': currency,
            'token': self.api_token
        }

        try:
            # Making the GET request
            response = requests.get(self.fetch_hotel_prices_url, params=params)
            # Check if the request was successful
            if response.status_code != 200:
                # Raise an exception if the response status code indicates failure
                raise Exception(f"Failed to fetch hotel prices. Status code: {response.status_code}")
            # Return the JSON content of the response
            return response.json()

        except requests.exceptions.RequestException as e:
            # Catch any request-related exceptions (e.g., timeouts, connection errors)
            raise Exception("There was an error making the request.") from e

    def fetch_hotel_collections(self, check_in, check_out, id, currency='rub', language='en', limit=10,
                                type='popularity'):
        """
        Fetches collections of hotels based on the provided parameters.

        Parameters:
        - check_in: Check-in date.
        - check_out: Check-out date.
        - currency: Currency of the response.
        - language: Language of the response.
        - limit: Limit on the number of hotels to return.
        - type: Types of hotels (refer to /tp/public/available_selections.json for options).
        - id: ID of the city (from the Cities request).

        Returns:
            A dictionary containing the hotel collection information. The structure includes:
            - 'hotel_id': Unique ID of the hotel.
            - 'distance': Distance from the hotel to the city center.
            - 'name': Name of the hotel.
            - 'stars': Number of stars.
            - 'rating': Rating of the hotel among visitors.
            - 'property_type': Type of the hotel (e.g., apartment, hotel, hostel).
            - 'hotel_type': Description of the hotel type.
            - 'last_price_info': Information about the last found price of the hotel (may not exist).
            - 'price': Cost of stay for the entire period with discount.
            - 'old_price': Cost of stay found before the discount.
            - 'discount': Discount size.
            - 'insertion_time': Time when the collection was found.
            - 'nights': Number of nights.
            - 'search_params': Search parameters:
                - 'adults': Number of adults.
                - 'children': Number of children.
                - 'checkIn': Check-in date.
                - 'checkOut': Check-out date.
                - 'price_pn': Cost per night in the hotel with discount.
                - 'old_price_pn': Cost per night in the hotel before the discount.
                - 'has_wifi': Availability of Wi-Fi in the hotel.
        """
        # Constructing the query string
        params = {
            'check_in': check_in,
            'check_out': check_out,
            'currency': currency,
            'language': language,
            'limit': limit,
            'type': type,
            'id': id,
            'token': self.api_token
        }

        try:
            # Making the GET request
            response = requests.get(self.fetch_hotel_collections_url, params=params)
            # Check if the request was successful
            if response.status_code != 200:
                # Raise an exception if the response status code indicates failure
                raise Exception(f"Failed to fetch hotel collections. Status code: {response.status_code}")
            # Return the JSON content of the response
            return response.json()

        except requests.exceptions.RequestException as e:
            # Catch any request-related exceptions (e.g., timeouts, connection errors)
            raise Exception("There was an error making the request.") from e

    def fetch_hotel_collection_types(self, city_id):
        """
        The request recovers the list of all available separate collections.
        This type is used to search for hotels with a discount.

        Parameters:
        - city_id: ID of the city.

        Returns:
            A dictionary containing the hotel collection types information. The structure includes:
            - 'center': Hotels located in the center of a city.
            - 'tophotels': Best hotels.
            - 'highprice': Most expensive hotels.
            - '3-stars', '4-stars', '5-stars': Automatic searching of hotels with 3, 4, or 5 stars.
            - 'restaurant': Availability of the hotel's own restaurant.
            - 'pets': Opportunity to live with pets.
            - 'pool': Availability of the hotel's own pool.
            - 'cheaphotel': Cheapest hotels.
            - 'luxury': Luxury hotels.
            - 'price': Manually formed collections by price.
            - 'rating': Hotels with the highest rating.
            - 'distance': Distance from an airport.
            - 'popularity': Popularity of a hotel.
            - '2stars', '3stars', '4stars', '5stars': Manually formed collections with the corresponding number of stars.
        """
        # Constructing the query string
        params = {
            'id': city_id,
            'token': self.api_token
        }

        try:
            # Making the GET request
            response = requests.get(self.fetch_hotel_collection_types_url, params=params)
            # Check if the request was successful
            if response.status_code != 200:
                # Raise an exception if the response status code indicates failure
                raise Exception(f"Failed to fetch hotel collection types. Status code: {response.status_code}")
            # Return the JSON content of the response
            return response.json()

        except requests.exceptions.RequestException as e:
            # Catch any request-related exceptions (e.g., timeouts, connection errors)
            raise Exception("There was an error making the request.") from e

    def fetch_room_types(self, language='en'):
        """
        Fetches room types

        Parameters:
        - language: Language of the response (e.g., pt, en, fr, de, id, it, pl, es, th, ru). Defaults to English ('en').

        Returns:
            A dictionary containing the room types information. The structure includes:
            Room type IDs as keys and room type names as values.
        """
        # Constructing the query string
        params = {
            'language': language,
            'token': self.api_token  # Assuming the token is stored as an instance variable
        }

        try:
            # Making the GET request
            response = requests.get(self.fetch_room_types_url, params=params)
            # Check if the request was successful
            if response.status_code != 200:
                # Raise an exception if the response status code indicates failure
                raise Exception(f"Failed to fetch room types. Status code: {response.status_code}")
            # Return the JSON content of the response
            return response.json()

        except requests.exceptions.RequestException as e:
            # Catch any request-related exceptions (e.g., timeouts, connection errors)
            raise Exception("There was an error making the request.") from e

    def fetch_hotel_types(self, language='en'):
        """
        Fetches hotel types

        Parameters:
        - language: Language of the response (e.g., pt, en, fr, de, id, it, pl, es, th, ru). Defaults to English ('en').

        Returns:
            A dictionary containing the hotel types information. The structure includes:
            Hotel type IDs as keys and hotel type names as values.
        """
        # Constructing the query string
        params = {
            'language': language,
            'token': self.api_token  # Assuming the token is stored as an instance variable
        }

        try:
            # Making the GET request
            response = requests.get(self.fetch_room_types_url, params=params)
            # Check if the request was successful
            if response.status_code != 200:
                # Raise an exception if the response status code indicates failure
                raise Exception(f"Failed to fetch room types. Status code: {response.status_code}")
            # Return the JSON content of the response
            return response.json()

        except requests.exceptions.RequestException as e:
            # Catch any request-related exceptions (e.g., timeouts, connection errors)
            raise Exception("There was an error making the request.") from e