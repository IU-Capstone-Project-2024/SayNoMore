import json

from api_collector.air_tickets.air_tickets_api import AirTicketsApi
from api_collector.hotels.hotel_api import HotelApi
import os


class Route:
    """
    This class creates a route consisting of air tickets and hotels.

    Attributes:
        origin (str): The starting point of the route.
        destination (str): The ending point of the route.
        departure_at (str): Departure date and time.
        return_at (str): Return date and time.
        budget (float, optional): The budget for the route.
        ticket (dict, optional): Information about the flight ticket.
        hotel (dict, optional): Information about the hotel.

    Methods:
        __init__(origin, destination, departure_at, return_at, budget=None, ticket=None, hotel=None):
            Initializes the Route instance with basic information and optional flight and hotel details.

        add_flight(ticket):
            Adds flight details to the route.

        add_hotel(hotel):
            Adds hotel details to the route.

        to_string():
            Returns a string representation of the route, including flight and hotel details.

        calculate_total_cost():
            Calculates the total cost of the route including both flight and hotel.
    """

    def __init__(self, origin, destination, departure_at, return_at, budget=None, ticket=None, hotel=None):
        """
        Initializes the Route instance.

        Parameters:
            origin (str): The starting point of the route.
            destination (str): The ending point of the route.
            departure_at (str): Departure date and time.
            return_at (str): Return date and time.
            budget (float, optional): The budget for the route.
            ticket (dict, optional): Information about the flight ticket.
            hotel (dict, optional): Information about the hotel.
        """
        self.origin = origin
        self.destination = destination
        self.departure_at = departure_at
        self.return_at = return_at
        self.budget = budget
        if ticket:
            self.add_flight(ticket)
        else:
            self.ticket = None
        if hotel:
            self.add_hotel(hotel)
        else:
            self.hotel = None

    def add_flight(self, ticket):
        """
        Adds flight details to the route.

        Parameters:
            ticket (dict): A dictionary containing flight details with the following keys:
                origin (str): Departure point
                destination (str): Destination point
                origin_airport (str): IATA code of the departure airport
                destination_airport (str): IATA code of the destination airport
                price (float): Ticket price
                airline (str): IATA code of the airline
                flight_number (str): Flight number
                departure_at (str): Departure date
                return_at (str): Return date
                transfers (int): Number of transfers on the outbound trip
                return_transfers (int): Number of transfers on the return trip
                duration (int): Total duration of the round trip in minutes
                duration_to (int): Duration of the outbound flight in minutes
                duration_back (int): Duration of the return flight in minutes
                link (str): Link to the ticket on Aviasales
                currency (str): Currency of the ticket price
        """
        self.ticket = ticket
        self.flight_origin = ticket['origin']
        self.flight_destination = ticket['destination']
        self.origin_airport = ticket['origin_airport']
        self.destination_airport = ticket['destination_airport']
        self.ticket_price = ticket['price']
        self.airline = ticket['airline']
        self.flight_number = ticket['flight_number']
        self.flight_departure_at = ticket['departure_at']
        self.flight_return_at = ticket['return_at']
        self.transfers = ticket['transfers']
        self.return_transfers = ticket['return_transfers']
        self.flight_duration = ticket['duration']
        self.flight_duration_to = ticket['duration_to']
        self.flight_duration_back = ticket['duration_back']
        self.flight_link = 'https://www.aviasales.com/' + ticket['link']

    def add_hotel(self, hotel):
        """
        Adds hotel details to the route.

        Parameters:
            hotel (dict): A dictionary containing hotel details with the following keys:
                locationId (int): ID of the location
                hotelId (int): ID of the hotel
                priceFrom (float): Minimum price for staying at the hotel room
                priceAvg (float): Average price for staying at the hotel room
                pricePercentile (dict): Price distribution by percentages
                stars (int): Number of stars of the hotel
                hotelName (str): Name of the hotel
                location (dict): Information about the hotel location
                geo (dict): Coordinates of the location (city)
                name (str): Name of the location (city)
                state (str): State where the city is located
                country (str): Country of the hotel
        """
        self.hotel = hotel
        self.hotel_location_id = hotel['locationId']
        self.hotel_id = hotel['hotelId']
        self.hotel_price_from = hotel['priceFrom']
        self.hotel_price_avg = hotel['priceAvg']
        self.hotel_price_percentile = hotel['pricePercentile']
        self.hotel_stars = hotel['stars']
        self.hotel_name = hotel['hotelName']
        self.hotel_location = hotel['location']
        self.hotel_geo = hotel['location']['geo']
        self.hotel_city_name = hotel['location']['name']
        self.hotel_state = hotel['location']['state']
        self.hotel_country = hotel['location']['country']

    def to_string(self):
        """
        Returns a string representation of the route including flight and hotel details.

        :return: str: A string describing the route, flight, and hotel details.
        """
        if self.ticket:
            flight_info = (f"Flight: {self.flight_origin} to {self.flight_destination}, "
                           f"Departing at: {self.flight_departure_at}, Returning at: {self.flight_return_at}, "
                           f"Airline: {self.airline}, Flight Number: {self.flight_number}, "
                           f"Price: {self.ticket_price} rub, "
                           f"Transfers: {self.transfers}, Return Transfers: {self.return_transfers}, "
                           f"Duration: {self.flight_duration} minutes")
        else:
            flight_info = 'No information about ticket'

        if self.hotel:
            hotel_info = (
                f"Hotel: {self.hotel_name}, Location: {self.hotel_city_name}, {self.hotel_state}, {self.hotel_country}, "
                f"Stars: {self.hotel_stars}, Price From: {self.hotel_price_from} rub, "
                f"Average Price: {self.hotel_price_avg} rub")
        else:
            hotel_info = 'No information about hotel'

        return f"Route from {self.origin} to {self.destination}:\n{flight_info}\n{hotel_info}"

    def calculate_total_cost(self):
        """
        Calculates the total cost of the route including both flight and hotel.

        :return: float: The total cost of the flight and hotel.
        """
        total_cost = 0
        if self.ticket:
            total_cost += self.ticket_price
        if self.hotel:
            total_cost += self.hotel_price_avg
        return total_cost


def get_ticket(origin, destination, departure_at=None, return_at=None, budget=None, number_of_tickets=1):
    """
    Fetch the cheapest air ticket based on the specified parameters.

    :param origin: str, IATA code of the departure point
    :param destination: str, IATA code of the destination point
    :param departure_at: str, optional, departure date (format YYYY-MM or YYYY-MM-DD)
    :param return_at: str, optional, return date (format YYYY-MM or YYYY-MM-DD)
    :param budget: float, optional, maximum price of the ticket
    :param number_of_tickets: amount of different tickets to return

    :return: list of dict, the cheapest tickets that matches the criteria:
        [{
                     "origin": str,  # Departure point
                     "destination": str,  # Destination point
                     "origin_airport": str,  # IATA code of the departure airport
                     "destination_airport": str,  # IATA code of the destination airport
                     "price": float,  # Ticket price
                     "airline": str,  # IATA code of the airline
                     "flight_number": str,  # Flight number
                     "departure_at": str,  # Departure date
                     "return_at": str,  # Return date
                     "transfers": int,  # Number of transfers on the outbound trip
                     "return_transfers": int,  # Number of transfers on the return trip
                     "duration": int,  # Total duration of the round trip in minutes
                     "duration_to": int,  # Duration of the outbound flight in minutes
                     "duration_back": int,  # Duration of the return flight in minutes
                     "link": str,  # Link to the ticket on Aviasales
                     "currency": str  # Currency of the ticket price
        }]
    """
    # Initialize an empty list to store tickets
    tickets = []
    # Loop through the first 9 pages to find tickets
    air_api = AirTicketsApi()
    for page in range(1, 10):
        # Fetch the cheapest tickets for the given parameters
        response = air_api.fetch_cheapest_tickets(origin=origin,
                                                  destination=destination,
                                                  departure_at=departure_at,
                                                  return_at=return_at,
                                                  one_way=True,
                                                  page=page)
        # Check if the response was successful
        if not response['success']:
            raise Exception('response was not successful')
        # Break the loop if no new ticket data is received
        if len(response['data']) == 0:
            break
        else:
            # Append the received ticket data to the tickets list
            tickets += response['data']
    # Filter tickets by budget if a budget is specified
    if budget:
        # Initialize the last index of the ticket list to include
        last_index = 0
        # Iterate through the tickets to find those within budget
        for i, ticket in enumerate(tickets):
            if ticket['price'] < budget:
                last_index = i
            else:
                break
        # Slice the tickets list to only include tickets within budget
        if len(tickets) <= number_of_tickets:
            return tickets
        else:
            min_index = max(0, last_index - (number_of_tickets // 2))
            max_index = min(len(tickets), last_index + (number_of_tickets // 2) + (number_of_tickets % 2))
            if max_index - min_index < number_of_tickets:
                if min_index == 0:
                    return tickets[:max_index]
                else:
                    return tickets[max_index-number_of_tickets:max_index]
            return tickets[min_index:max_index]
    else:
        return tickets[:number_of_tickets] if len(tickets) > number_of_tickets else tickets


def get_hotel(location, check_in, check_out, budget=None, min_stars=0):
    """
    Fetches the hotel based on the specified parameters.

    Parameters:
    :param location: str, Name of the location (can use IATA code).
    :param check_in: str, Check-in date (format YYYY-MM-DD).
    :param check_out: str, Check-out date (format YYYY-MM-DD).
    :param budget: float, optional, Maximum price for the hotel.
    :param min_stars: min number of stars for hotel required

    :return: dict: The hotel that matches the criteria or None if no hotels match:
        {
            'locationId': int,  # ID of the location
            'hotelId': int,  # ID of the hotel
            'priceFrom': float,  # Minimum price for staying at the hotel room
            'priceAvg': float,  # Average price for staying at the hotel room
            'pricePercentile': dict,  # Price distribution by percentages
            'stars': int,  # Number of stars of the hotel
            'hotelName': str,  # Name of the hotel
            'location': dict,  # Information about the hotel location
            'geo': dict,  # Coordinates of the location (city)
            'name': str,  # Name of the location (city)
            'state': str,  # State where the city is located
            'country': str  # Country of the hotel
        }
    """
    hotel_api = HotelApi()
    # Fetch hotel prices based on the provided location, check-in and check-out dates, and limit
    hotels = hotel_api.fetch_hotel_prices(location=location,
                                          check_in=check_in,
                                          check_out=check_out,
                                          limit=10000)
    # check if we fetched at least one hotel
    if len(hotels) == 0:
        return None

    # get all hotel ids satisfied our filter
    filtered_hotels = find_filtered_hotels(locationId=hotels[0]['locationId'], min_stars=min_stars)
    # filter obtained hotels
    hotels[:] = [hotel for hotel in hotels if hotel['hotelId'] in filtered_hotels]
    # check if we filtered at least one hotel
    if len(hotels) == 0:
        return None

    # Sort the fetched hotels by the 'priceFrom' field in ascending order
    hotels = sorted(hotels, key=lambda x: x['priceFrom'])

    # If a budget is specified, filter hotels to include only those with 'priceFrom' less than the budget
    if budget:
        hotels = [hotel for hotel in hotels if hotel['priceFrom'] < budget]
    else:
        return hotels[0] if len(hotels) > 0 else None

    # Return the last hotel in the filtered list (the cheapest within budget), or None if no hotels match
    if len(hotels) > 0:
        return hotels[-1]
    else:
        return None


def find_top_routes(origin, destination, departure_at=None, return_at=None, budget=None, route_number=3, min_stars=0) -> \
list[Route]:
    """
    Find the top routes based on the cheapest tickets and hotels.

    Parameters:
    :param origin: str, IATA code of the departure point.
    :param destination: str, IATA code of the destination point.
    :param departure_at: str, optional, departure date (format YYYY-MM-DD).
    :param return_at: str, optional, return date (format YYYY-MM-DD).
    :param budget: float, optional, maximum combined price for the ticket and hotel.
    :param route_number: int, optional, number of top routes to find (default is 3).
    :param min_stars: min number of stars for hotel required

    :return: list of 'Route' class
    """
    # Get the cheapest ticket and hotel
    cheapest_ticket = get_ticket(origin=origin, destination=destination, departure_at=departure_at,
                                 return_at=return_at)
    cheapest_hotel = get_hotel(location=destination, check_in=departure_at, check_out=return_at, min_stars=min_stars)

    # Create a return array with the initial cheapest route
    top_routes = [{
        'ticket': cheapest_ticket,
        'hotel': cheapest_hotel
    }]

    # Define minimum prices
    min_ticket_price = cheapest_ticket['price']
    min_hotel_price = cheapest_hotel['priceFrom']

    # Check if budget is specified
    if budget:
        # Check if the cheapest route exceeds the budget
        if cheapest_hotel['priceFrom'] + cheapest_ticket['price'] > budget:
            # cheapest route exceed the budsget, return the cheapest route
            return [Route(origin=origin, destination=destination, departure_at=departure_at, return_at=return_at,
                          budget=budget, ticket=top_routes[0]['ticket'], hotel=top_routes[0]['hotel'])]
        else:
            # Make return value empty
            top_routes = []
            # Define part of a budget for tickets and hotels
            coef = min_ticket_price / (min_ticket_price + min_hotel_price)
            ticket_price = max(coef * budget * 0.9, min_ticket_price)

            ticket = get_ticket(origin=origin, destination=destination, departure_at=departure_at,
                                return_at=return_at, budget=ticket_price)
            hotel_price = budget - ticket['price']
            hotel = get_hotel(location=destination, check_in=departure_at, check_out=return_at,
                              budget=hotel_price, min_stars=min_stars)
            top_routes.append({
                'ticket': ticket,
                'hotel': hotel
            })
            ticket_price *= 1.1
            hotel_price *= 1.1
    else:
        # Budget is not specified, finding arbitrary routes
        for _ in range(1, route_number):
            min_ticket_price *= 2
            ticket = get_ticket(origin=origin, destination=destination, departure_at=departure_at,
                                return_at=return_at, budget=min_ticket_price)
            min_hotel_price *= 3
            hotel = get_hotel(location=destination, check_in=departure_at, check_out=return_at,
                              budget=min_hotel_price, min_stars=min_stars)
            top_routes.append({
                'ticket': ticket,
                'hotel': hotel
            })

    # Remove duplicates and convert to Route class
    unique_routes = []
    for i in range(len(top_routes)):
        if i == 0 or (top_routes[i]['ticket'] != top_routes[i - 1]['ticket'] or top_routes[i]['hotel'] !=
                      top_routes[i - 1]['hotel']):
            unique_routes.append(
                Route(origin=origin, destination=destination, departure_at=departure_at, return_at=return_at,
                      budget=budget, ticket=top_routes[i]['ticket'], hotel=top_routes[i]['hotel']))
    return unique_routes


def find_filtered_hotels(locationId, filter=(1, 2, 3, 12), min_stars=0):
    """
    This function filters hotels based on their type
    :param locationId: location of hotels
    :param filter: hotels types which will be chosen. More information about filters is saved in
        data/hotels/hotels_type.json directory or can be obtained by 'fetch_hotel_types' method in HotelApi class
    :param min_stars: min number of stars for hotel required
    :return: list of all suitable hotels ids
    """
    hotel_api = HotelApi()
    # check if we have already saved information about hotels in given location
    file_path = hotel_api.data_directory_path() + hotel_api.hotels_list_dir + f'/{locationId}.json'
    if not os.path.exists(file_path):
        data = hotel_api.fetch_hotel_list(locationId=locationId)
    else:
        with open(file_path) as f:
            data = json.load(f)

    # list of chosen hotels
    filtered_hotels = []
    # iterate through all hotels and choose one which satisfy the condition
    for hotel in data['hotels']:
        if hotel['propertyType'] in filter:
            if hotel['stars'] >= min_stars:
                filtered_hotels.append(hotel['id'])

    # return list of chosen hotels
    return filtered_hotels
