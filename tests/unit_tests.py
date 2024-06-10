from unittest import TestCase, main
from air_tickets.air_tickets_api import AirTicketsApi
from datetime import datetime, timedelta

class TestAirTicketsApi(TestCase):
    def setUp(self):
        self.api = AirTicketsApi()

    def test_fetch_cheapest_tickets(self):
        expected_data = {
            'origin' : "MOW",
            'destination' : "DXB"
        }

        response = self.api.fetch_cheapest_tickets(origin='MOW', destination='DXB')
        self.assertTrue(response['success'])
        self.assertEqual(response['data'][0]['origin'], expected_data['origin'])
        self.assertEqual(response['data'][0]['destination'], expected_data['destination'])

    def test_fetch_grouped_tickets(self):
        expected_data = {
            'origin': "MOW",
            'destination': "DXB"
        }
        today = datetime.today()
        two_weeks_later = today + timedelta(weeks=2)
        departure_date = two_weeks_later.strftime('%Y-%m-%d')

        response = self.api.fetch_grouped_tickets(origin='MOW', destination='DXB', departure_at=departure_date)
        self.assertTrue(response['success'])
        self.assertEqual(response['data'][departure_date]['origin'], expected_data['origin'])
        self.assertEqual(response['data'][departure_date]['destination'], expected_data['destination'])

    def test_fetch_period_tickets(self):
        expected_data = {
            'origin': "MOW",
            'destination': "DXB"
        }
        today = datetime.today()
        two_weeks_later = today + timedelta(weeks=2)
        beginning_of_period = two_weeks_later.strftime('%Y-%m-%d')

        response = self.api.fetch_period_tickets(origin='MOW', destination='DXB', beginning_of_period=beginning_of_period)
        self.assertTrue(response['success'])
        self.assertEqual(response['data'][0]['origin'], expected_data['origin'])
        self.assertEqual(response['data'][0]['destination'], expected_data['destination'])

if __name__ == '__main__':
    main()