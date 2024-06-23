from unittest import TestCase, main
from api_collector.air_tickets.air_tickets_api import AirTicketsApi
from api_collector.hotels.hotel_api import HotelApi
from datetime import datetime, timedelta
import os


# Define a class that inherits from TestCase to create unit tests for the AirTicketsApi
class TestAirTicketsApi(TestCase):

    def setUp(
            self):  # This method is called before each test method is executed
        # Initialize an instance of AirTicketsApi for use in the tests
        self.air_api = AirTicketsApi()
        self.hotel_api = HotelApi()

    def test_fetch_cheapest_tickets(
            self):  # Test method for fetching cheapest tickets
        # Define expected data structure for comparison
        expected_data = {
            'origin': "MOW",  # Moscow (IATA: MOW) as origin
            'destination': "DXB"  # Dubai (IATA: DXB) as destination
        }

        # Call the fetch_cheapest_tickets method on the api object and store its response
        response = self.air_api.fetch_cheapest_tickets(origin='MOW',
                                                       destination='DXB')

        # Assert that the response indicates success
        self.assertTrue(response['success'])
        # Assert that the first ticket in the response matches the expected origin and destination
        self.assertEqual(response['data'][0]['origin'],
                         expected_data['origin'])
        self.assertEqual(response['data'][0]['destination'],
                         expected_data['destination'])

    def test_fetch_grouped_tickets(
        self
    ):  # Test method for fetching grouped tickets based on departure date
        # Define expected data structure for comparison
        expected_data = {'origin': "MOW", 'destination': "DXB"}
        # Get today's date and calculate the date two weeks later
        today = datetime.today()
        two_weeks_later = today + timedelta(weeks=2)
        # Format the departure date as a string in YYYY-MM-DD format
        departure_date = two_weeks_later.strftime('%Y-%m-%d')

        # Call the fetch_grouped_tickets method on the api object and store its response
        response = self.air_api.fetch_grouped_tickets(
            origin='MOW', destination='DXB', departure_at=departure_date)

        # Assert that the response indicates success
        self.assertTrue(response['success'])
        # Assert that the ticket for the calculated departure date matches the expected origin and destination
        self.assertEqual(response['data'][departure_date]['origin'],
                         expected_data['origin'])
        self.assertEqual(response['data'][departure_date]['destination'],
                         expected_data['destination'])

    def test_fetch_period_tickets(
            self):  # Test method for fetching tickets within a specific period
        # Define expected data structure for comparison
        expected_data = {'origin': "MOW", 'destination': "DXB"}
        # Get today's date and calculate the date two weeks later
        today = datetime.today()
        two_weeks_later = today + timedelta(weeks=2)
        # Calculate the start of the period as the day after the departure date
        beginning_of_period = two_weeks_later.strftime('%Y-%m-%d')

        # Call the fetch_period_tickets method on the api object and store its response
        response = self.air_api.fetch_period_tickets(
            origin='MOW',
            destination='DXB',
            beginning_of_period=beginning_of_period)

        # Assert that the response indicates success
        self.assertTrue(response['success'])
        # Assert that the first ticket in the response matches the expected origin and destination
        self.assertEqual(response['data'][0]['origin'],
                         expected_data['origin'])
        self.assertEqual(response['data'][0]['destination'],
                         expected_data['destination'])

    def test_fetch_alternative_route_tickets(self):
        response = self.air_api.fetch_alternative_route_tickets(
            origin='OVB', destination='LED')
        # Check if 'prices' key exists in the response and contains at least one item
        assert 'prices' in response, "'prices' key not found in the response."
        assert len(response['prices']) > 0, "No prices found in the response."

    def test_fetch_popular_routes_from_city(self):
        response = self.air_api.fetch_popular_routes_from_city(origin='MOW')
        # Assert that the response indicates success
        self.assertTrue(response['success'])

    def test_fetch_airline_logo(self):
        iata_code = 'UN'
        file_path = f'photos/airline_logos/{iata_code}.png'
        # Check if the file exists
        if os.path.exists(file_path):
            # Delete the file
            os.remove(file_path)
        self.assertFalse(os.path.exists(file_path))
        # check api
        self.air_api.fetch_airline_logo(f'{iata_code}')
        # check for logo existence
        self.assertTrue(os.path.exists(file_path))

    def test_search_hotel_or_location(self):
        expected_data = {'status': 'ok'}
        query = 'moscow'
        response = self.hotel_api.search_hotel_or_location(query=query)
        self.assertEqual(response['status'], expected_data['status'])

    def test_fetch_hotel_prices(self):
        location = 'moscow'
        # Get today's date and calculate the date two weeks later
        today = datetime.today()
        two_weeks_later = today + timedelta(weeks=2)
        three_weeks_later = today + timedelta(weeks=3)
        # Format the departure date as a string in YYYY-MM-DD format
        check_in = two_weeks_later.strftime('%Y-%m-%d')
        check_out = three_weeks_later.strftime('%Y-%m-%d')
        response = self.hotel_api.fetch_hotel_prices(location=location,
                                                     check_in=check_in,
                                                     check_out=check_out)
        self.assertTrue(response[0]['locationId'])

    def test_fetch_hotel_collections(self):
        city_id = 12209
        today = datetime.today()
        two_weeks_later = today + timedelta(weeks=2)
        three_weeks_later = today + timedelta(weeks=3)
        # Format the departure date as a string in YYYY-MM-DD format
        check_in = two_weeks_later.strftime('%Y-%m-%d')
        check_out = three_weeks_later.strftime('%Y-%m-%d')
        response = self.hotel_api.fetch_hotel_collections(city_id=city_id,
                                                          check_in=check_in,
                                                          check_out=check_out)
        self.assertTrue(response['popularity'])

    def test_fetch_hotel_collection_types(self):
        id = 12209
        response = self.hotel_api.fetch_hotel_collection_types(city_id=id)
        self.assertTrue(len(response) > 0)

    def test_fetch_room_types(self):
        response = self.hotel_api.fetch_hotel_types()
        self.assertTrue(response['1'])

    def test_fetch_hotel_types(self):
        response = self.hotel_api.fetch_hotel_types()
        self.assertTrue(response['1'])

    def test_fetch_hotel_photos(self):
        id = [4]
        file_path = f'photos/hotelPhotos/4/photo1.avif'
        # Check if the file exists
        if os.path.exists(file_path):
            # Delete the file
            os.remove(file_path)
        self.assertFalse(os.path.exists(file_path))
        # check api
        self.hotel_api.fetch_hotel_photos(id)
        # check for logo existence
        self.assertTrue(os.path.exists(file_path))

    def test_fetch_city_photo(self):
        iata_code = 'MOW'
        file_path = f'photos/cityPhotos/{iata_code}.png'
        # Check if the file exists
        if os.path.exists(file_path):
            # Delete the file
            os.remove(file_path)
        self.assertFalse(os.path.exists(file_path))
        # check api
        self.hotel_api.fetch_city_photo(iata_code)
        # check for logo existence
        self.assertTrue(os.path.exists(file_path))


if __name__ == '__main__':
    main()
