from unittest import TestCase, main
from air_tickets.air_tickets_api import AirTicketsApi

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

if __name__ == '__main__':
    main()