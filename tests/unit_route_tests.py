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

        # Check the returned ticket
        self.assertEqual(ticket['origin'], 'JFK')
        self.assertEqual(ticket['destination'], 'LAX')
        self.assertEqual(ticket['price'], 150.0)
        self.assertEqual(ticket['airline'], 'AA')

    @patch('route.route_collector.HotelApi')  # Adjust the import path as needed
    def test_get_hotel_with_budget(self, MockHotelApi):
        # Set up the mock response
        mock_api_instance = MockHotelApi.return_value
        mock_api_instance.fetch_hotel_prices.return_value = [
            {
                'locationId': 12186,
                'hotelId': 1405139619,
                'priceFrom': 24619.74,
                'priceAvg': 24619.74,
                'pricePercentile': {'3': 24619.74, '10': 24619.74, '35': 24619.74, '50': 24619.74, '75': 24619.74,
                                    '99': 24619.74},
                'stars': 4,
                'hotelName': 'AMAKS Congress Hotel',
                'location': {'name': 'Ryazan', 'country': 'Russia', 'state': None,
                             'geo': {'lat': 54.619779, 'lon': 39.744939}}
            },
            {
                'locationId': 12186,
                'hotelId': 546032,
                'priceFrom': 24019.25,
                'priceAvg': 24019.25,
                'pricePercentile': {'3': 24019.25, '10': 24019.25, '35': 24019.25, '50': 24019.25, '75': 24019.25,
                                    '99': 24019.25},
                'stars': 4,
                'hotelName': 'Congress Hotel Forum',
                'location': {'name': 'Ryazan', 'country': 'Russia', 'state': None,
                             'geo': {'lat': 54.619779, 'lon': 39.744939}}
            },
            {
                'locationId': 12186,
                'hotelId': 714884,
                'priceFrom': 20446.39,
                'priceAvg': 20446.39,
                'pricePercentile': {'3': 20446.39, '10': 20446.39, '35': 20446.39, '50': 20446.39, '75': 20446.39,
                                    '99': 20446.39},
                'stars': 3,
                'hotelName': 'Aragon Hotel',
                'location': {'name': 'Ryazan', 'country': 'Russia', 'state': None,
                             'geo': {'lat': 54.619779, 'lon': 39.744939}}
            },
            {
                'locationId': 12186,
                'hotelId': 40972234,
                'priceFrom': 18014.44,
                'priceAvg': 18014.44,
                'pricePercentile': {'3': 18014.44, '10': 18014.44, '35': 18014.44, '50': 18014.44, '75': 18014.44,
                                    '99': 18014.44},
                'stars': 3,
                'hotelName': 'Ryazan Hotel',
                'location': {'name': 'Ryazan', 'country': 'Russia', 'state': None,
                             'geo': {'lat': 54.619779, 'lon': 39.744939}}
            },
            {
                'locationId': 12186,
                'hotelId': 714887,
                'priceFrom': 13811.07,
                'priceAvg': 13811.07,
                'pricePercentile': {'3': 13811.07, '10': 13811.07, '35': 13811.07, '50': 13811.07, '75': 13811.07,
                                    '99': 13811.07},
                'stars': 2,
                'hotelName': 'Lovech Sport',
                'location': {'name': 'Ryazan', 'country': 'Russia', 'state': None,
                             'geo': {'lat': 54.619779, 'lon': 39.744939}}
            }
        ]

        collector = RouteCollector()

        # Call the method with a budget
        hotel = collector.get_hotel(location='Ryazan', check_in='2024-07-01', check_out='2024-07-10', budget=20000)

        # Check the returned hotel
        self.assertIsNotNone(hotel)
        self.assertEqual(hotel['hotelId'], 40972234)
        self.assertEqual(hotel['priceFrom'], 18014.44)

    @patch('route.route_collector.RouteCollector.get_ticket')  # Adjust the import path as needed
    @patch('route.route_collector.RouteCollector.get_hotel')  # Adjust the import path as needed
    def test_find_top_routes_with_budget(self, mock_get_hotel, mock_get_ticket):
        # Set up the mock responses
        mock_get_ticket.return_value = {
            'origin': 'JFK',
            'destination': 'LAX',
            'price': 150.0,
            'airline': 'AA',
            'flight_number': 'AA100',
            'departure_at': '2024-07-01',
            'return_at': '2024-07-15',
            'transfers': 0,
            'return_transfers': 0,
            'duration': 300,
            'duration_to': 300,
            'duration_back': 300,
            'link': 'http://example.com/ticket1',
            'currency': 'USD'
        }

        mock_get_hotel.return_value = {
            'locationId': 12186,
            'hotelId': 714884,
            'priceFrom': 100.0,
            'priceAvg': 100.0,
            'pricePercentile': {'3': 100.0, '10': 100.0, '35': 100.0, '50': 100.0, '75': 100.0, '99': 100.0},
            'stars': 3,
            'hotelName': 'Aragon Hotel',
            'location': {'name': 'Ryazan', 'country': 'Russia', 'state': None,
                         'geo': {'lat': 54.619779, 'lon': 39.744939}}
        }

        collector = RouteCollector()

        # Call the method with a budget
        routes = collector.find_top_routes(origin='JFK', destination='LAX', departure_at='2024-07-01',
                                           return_at='2024-07-15', budget=300.0, route_number=2)

        # Check the returned routes
        self.assertEqual(len(routes), 1)
        self.assertEqual(routes[0]['ticket']['price'], 150.0)
        self.assertEqual(routes[0]['hotel']['priceFrom'], 100.0)


if __name__ == '__main__':
    unittest.main()
