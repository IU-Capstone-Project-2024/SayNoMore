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
                - 'id': ID of the location in the database.
                - 'type': Type of the location (e.g., City, Island).
                - 'countryIso': ISO code of the country.
                - 'name': Name of the location.
                - 'state': State code, if applicable.
                - 'fullname': Full name of the location including the country name.
                - 'geo': Geographical coordinates of the location.
                    - 'lat': Latitude.
                    - 'lon': Longitude.
            - 'hotels': A list of hotel objects. Each object contains:
                - 'id': ID of the hotel in the database.
                - 'name': Name of the hotel.
                - 'locationId': ID of the location where the hotel is located.
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
            'token' : self.api_token
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