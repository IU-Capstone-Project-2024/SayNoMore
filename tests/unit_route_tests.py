import unittest
from unittest.mock import patch, MagicMock
from route.route_collector import RouteCollector


class TestRouteCollector(unittest.TestCase):


    @patch('route.route_collector.AirTicketsApi')  # Mock the AirTicketsApi class
    def test_get_ticket_with_budget(self, MockAirTicketsApi):
        # Set up the mock response
        mock_api_instance = MockAirTicketsApi.return_value
        mock_api_instance.fetch_cheapest_tickets.side_effect = [
            {
                'success': True,
                'data': [
                    {
                        "origin": "JFK",
                        "destination": "LAX",
                        "origin_airport": "JFK",
                        "destination_airport": "LAX",
                        "price": 150.0,
                        "airline": "AA",
                        "flight_number": "AA100",
                        "departure_at": "2024-07-01",
                        "return_at": "2024-07-15",
                        "transfers": 0,
                        "return_transfers": 0,
                        "duration": 300,
                        "duration_to": 300,
                        "duration_back": 300,
                        "link": "http://example.com/ticket1",
                        "currency": "USD"
                    },
                    {
                        "origin": "JFK",
                        "destination": "LAX",
                        "origin_airport": "JFK",
                        "destination_airport": "LAX",
                        "price": 300.0,
                        "airline": "AA",
                        "flight_number": "AA101",
                        "departure_at": "2024-07-01",
                        "return_at": "2024-07-15",
                        "transfers": 0,
                        "return_transfers": 0,
                        "duration": 300,
                        "duration_to": 300,
                        "duration_back": 300,
                        "link": "http://example.com/ticket2",
                        "currency": "USD"
                    }
                ]
            },
            {'success': True, 'data': []}  # No more data on the second page
        ]

        collector = RouteCollector()

        # Call the method with a budget
        ticket = collector.get_ticket(origin='JFK', destination='LAX', departure_at='2024-07-01',
                                      return_at='2024-07-15',
                                      budget=200.0)
        print(ticket)

        # Check the returned ticket
        self.assertEqual(ticket['origin'], 'JFK')
        self.assertEqual(ticket['destination'], 'LAX')
        self.assertEqual(ticket['price'], 150.0)
        self.assertEqual(ticket['airline'], 'AA')


if __name__ == '__main__':
    unittest.main()
