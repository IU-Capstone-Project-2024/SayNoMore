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

