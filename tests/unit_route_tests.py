import unittest
from unittest.mock import patch
from api_collector.route.route import Route, get_hotel, get_ticket, find_top_routes


class TestRouteCollector(unittest.TestCase):

    @patch('api_collector.route.route.AirTicketsApi')  # Mock the AirTicketsApi class
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

        # Call the method with a budget
        tickets = get_ticket(origin='JFK', destination='LAX', departure_at='2024-07-01',
                                      return_at='2024-07-15',
                                      budget=200.0)

        # Check the returned ticket
        self.assertEqual(tickets[0].flight_origin, 'JFK')
        self.assertEqual(tickets[0].flight_destination, 'LAX')
        self.assertEqual(tickets[0].ticket_price, 150.0)
        self.assertEqual(tickets[0].airline, 'AA')


    @patch('api_collector.route.route.HotelApi')
    @patch('api_collector.route.route.find_filtered_hotels')
    def test_get_hotel_with_budget(self, mock_find_filtered_hotels, mock_HotelApi):
        # Setup mock responses
        hotels = [
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
        mock_HotelApi.return_value.fetch_hotel_prices.return_value = hotels
        mock_find_filtered_hotels.return_value = [1, 2, 40972234]

        # get result
        result = get_hotel(location='Ryazan', check_in='2024-07-01', check_out='2024-07-10', budget=20000)
        expected_hotel = {
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
            }

        # asses result
        self.assertEqual(result[0], expected_hotel)

    @patch('api_collector.route.route.get_ticket')
    @patch('api_collector.route.route.get_hotel')
    def test_find_top_routes_with_budget(self, mock_get_hotel, mock_get_ticket):
        # Set up the mock responses
        mock_get_ticket.return_value = [{
            'origin': 'JFK',
            'destination': 'LAX',
            "origin_airport": "JFK",
            "destination_airport": "LAX",
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
        }]

        mock_get_hotel.return_value = [{
            'locationId': 12186,
            'hotelId': 714884,
            'priceFrom': 100.0,
            'priceAvg': 100.0,
            'pricePercentile': {'3': 100.0, '10': 100.0, '35': 100.0, '50': 100.0, '75': 100.0, '99': 100.0},
            'stars': 3,
            'hotelName': 'Aragon Hotel',
            'location': {'name': 'Ryazan', 'country': 'Russia', 'state': None,
                         'geo': {'lat': 54.619779, 'lon': 39.744939}}
        }]

        # Call the method with a budget
        routes = find_top_routes(origin='JFK', destination='LAX', departure_at='2024-07-01',
                                           return_at='2024-07-15', budget=300.0, route_number=2)

        # Check the returned routes
        self.assertEqual(len(routes), 1)
        self.assertEqual(routes[0].ticket_price, 150.0)
        self.assertEqual(routes[0].hotel_price_from, 100.0)


if __name__ == '__main__':
    unittest.main()