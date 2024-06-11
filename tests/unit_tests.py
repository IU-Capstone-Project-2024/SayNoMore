from unittest import TestCase, main
from air_tickets.air_tickets_api import AirTicketsApi
from datetime import datetime, timedelta


# Define a class that inherits from TestCase to create unit tests for the AirTicketsApi
class TestAirTicketsApi(TestCase):
    def setUp(self):  # This method is called before each test method is executed
        # Initialize an instance of AirTicketsApi for use in the tests
        self.api = AirTicketsApi()

    def test_fetch_cheapest_tickets(self):  # Test method for fetching cheapest tickets
        # Define expected data structure for comparison
        expected_data = {
            'origin': "MOW",  # Moscow (IATA: MOW) as origin
            'destination': "DXB"  # Dubai (IATA: DXB) as destination
        }

        # Call the fetch_cheapest_tickets method on the api object and store its response
        response = self.api.fetch_cheapest_tickets(origin='MOW', destination='DXB')

        # Assert that the response indicates success
        self.assertTrue(response['success'])
        # Assert that the first ticket in the response matches the expected origin and destination
        self.assertEqual(response['data'][0]['origin'], expected_data['origin'])
        self.assertEqual(response['data'][0]['destination'], expected_data['destination'])

    def test_fetch_grouped_tickets(self):  # Test method for fetching grouped tickets based on departure date
        # Define expected data structure for comparison
        expected_data = {
            'origin': "MOW",
            'destination': "DXB"
        }
        # Get today's date and calculate the date two weeks later
        today = datetime.today()
        two_weeks_later = today + timedelta(weeks=2)
        # Format the departure date as a string in YYYY-MM-DD format
        departure_date = two_weeks_later.strftime('%Y-%m-%d')

        # Call the fetch_grouped_tickets method on the api object and store its response
        response = self.api.fetch_grouped_tickets(origin='MOW', destination='DXB', departure_at=departure_date)

        # Assert that the response indicates success
        self.assertTrue(response['success'])
        # Assert that the ticket for the calculated departure date matches the expected origin and destination
        self.assertEqual(response['data'][departure_date]['origin'], expected_data['origin'])
        self.assertEqual(response['data'][departure_date]['destination'], expected_data['destination'])

    def test_fetch_period_tickets(self):  # Test method for fetching tickets within a specific period
        # Define expected data structure for comparison
        expected_data = {
            'origin': "MOW",
            'destination': "DXB"
        }
        # Get today's date and calculate the date two weeks later
        today = datetime.today()
        two_weeks_later = today + timedelta(weeks=2)
        # Calculate the start of the period as the day after the departure date
        beginning_of_period = two_weeks_later.strftime('%Y-%m-%d')

        # Call the fetch_period_tickets method on the api object and store its response
        response = self.api.fetch_period_tickets(origin='MOW', destination='DXB',
                                                 beginning_of_period=beginning_of_period)

        # Assert that the response indicates success
        self.assertTrue(response['success'])
        # Assert that the first ticket in the response matches the expected origin and destination
        self.assertEqual(response['data'][0]['origin'], expected_data['origin'])
        self.assertEqual(response['data'][0]['destination'], expected_data['destination'])

    def test_fetch_alternative_route_tickets(self):
        response = self.api.fetch_alternative_route_tickets(origin='OVB', destination='LED')
        # Check if 'prices' key exists in the response and contains at least one item
        assert 'prices' in response, "'prices' key not found in the response."
        assert len(response['prices']) > 0, "No prices found in the response."

if __name__ == '__main__':
    main()
