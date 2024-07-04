import json
from api_collector.utils.directories import data_directory_path
from api_collector.air_tickets.air_tickets_api import AirTicketsApi
from api_collector.hotels.hotel_api import HotelApi
import os


class Ticket:
    def __init__(self, ticket):
        """
                Initialize ticket information

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
        self.flight_link = 'https://www.aviasales.com' + ticket['link']

    def to_string(self):
        flight_info = (f"Flight Information:\n"
                       f"From: {self.flight_origin} ({self.origin_airport})\n"
                       f"To: {self.flight_destination} ({self.destination_airport})\n"
                       f"Airline: {self.airline}\n"
                       f"Flight Number: {self.flight_number}\n"
                       f"Departure: {self.flight_departure_at}\n"
                       f"Return: {self.flight_return_at}\n"
                       f"Price: {self.ticket_price} rub\n"
                       f"Transfers (outbound): {self.transfers}\n"
                       f"Transfers (return): {self.return_transfers}\n"
                       f"Outbound Duration: {self.flight_duration_to // 60} hours {self.flight_duration_to % 60} minutes\n"
                       f"Return Duration: {self.flight_duration_back // 60} hours {self.flight_duration_back % 60} minutes\n")

        return flight_info

class Hotel:
    def __init__(self, hotel):
        """
        Initialize hotel information

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
        self.photo_urls = []

    def to_string(self):
        hotel_info = (f"Hotel Information:\n"
                      f"Hotel Name: {self.hotel_name}\n"
                      f"Location: {self.hotel_city_name}, {self.hotel_state}, {self.hotel_country}\n"
                      f"Stars: {self.hotel_stars}\n"
                      f"Prices from: {self.hotel_price_from} rub\n")

        return hotel_info

class Route:
    """
    This class creates a route consisting of air tickets and hotels.

    Attributes:
        origin (str): The starting point of the route.
        destination (str): The ending point of the route.
        departure_at (str): Departure date and time.
        return_at (str): Return date and time.
        budget (float, optional): The budget for the route.
        ticket (Ticket, optional): Information about the flight ticket.
        hotel (Hotel, optional): Information about the hotel.

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
            self.ticket = ticket
        else:
            self.ticket = None
        if hotel:
            self.hotel = hotel
        else:
            self.hotel = None

    def add_flight(self, ticket):
        """
        Adds flight details to the route.
        """
        self.ticket = Ticket(ticket=ticket)

    def add_hotel(self, hotel):
        """
        Adds hotel details to the route.

        """
        self.hotel = Hotel(hotel=hotel)

    def to_string(self):
        """
        Returns a string representation of the route including flight and hotel details.

        :return: str: A string describing the route, flight, and hotel details.
        """
        if self.ticket:
            flight_info = self.ticket.to_string()
        else:
            flight_info = 'No information about ticket'

        if self.hotel:
            hotel_info = self.hotel.to_string()
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
            total_cost += self.ticket.ticket_price
        if self.hotel:
            total_cost += self.hotel.hotel_price_from
        return total_cost


def get_ticket(origin, destination, departure_at=None, return_at=None, budget=None, number_of_tickets=1,
               max_transfers=0, airlines=(), max_flight_duration=None) -> list[Ticket]:
    """
    Fetch the cheapest air ticket based on the specified parameters.

    :param origin: str, IATA code of the departure point
    :param destination: str, IATA code of the destination point
    :param departure_at: str, optional, departure date (format YYYY-MM or YYYY-MM-DD)
    :param return_at: str, optional, return date (format YYYY-MM or YYYY-MM-DD)
    :param budget: float, optional, maximum price of the ticket
    :param number_of_tickets: amount of different tickets to return
    :param max_transfers: max number of transfers during a flight, 0 by default
    :param airlines: list of airlines which are required for a flight, by default empty tuple - all airlines are allowed
    :param max_flight_duration: max duration of a flight in hours, None by default

    :return: list of tickets of class 'Ticket'
    """
    # Initialize an empty list to store tickets
    tickets = []
    # Loop through the first 9 pages to find tickets
    air_api = AirTicketsApi()
    # find tickets
    if max_transfers == 0:
        for page in range(1, 10):
            # Fetch the cheapest tickets for the given parameters
            response = air_api.fetch_cheapest_tickets(origin=origin,
                                                      destination=destination,
                                                      departure_at=departure_at,
                                                      return_at=return_at,
                                                      one_way=True,
                                                      direct=True,
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
    if len(tickets) == 0 or max_transfers != 0:
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

    # filter tickets by number of transfers
    if max_transfers > 0:
        tickets[:] = [ticket for ticket in tickets if
                      ticket['transfers'] <= max_transfers and ticket['return_transfers'] <= max_transfers]

    # filter by airline
    if len(airlines) > 0:
        tickets[:] = [ticket for ticket in tickets if
                      ticket['airline'] in airlines]

    # filter by flight duration
    if max_flight_duration:
        tickets[:] = [ticket for ticket in tickets if
                      ticket['duration_to'] / 60 <= max_flight_duration and ticket[
                          'duration_back'] / 60 <= max_flight_duration]

    # Filter tickets by budget if a budget is specified
    if len(tickets) == 0:
        return None
    if budget and (not budget == "None"):
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
            return conver_to_Ticket_class(tickets)
        else:
            min_index = max(0, last_index - (number_of_tickets // 2))
            max_index = min(len(tickets), last_index + (number_of_tickets // 2) + (number_of_tickets % 2))
            if max_index - min_index < number_of_tickets:
                if min_index == 0:
                    return conver_to_Ticket_class(tickets[:number_of_tickets])
                else:
                    return conver_to_Ticket_class(tickets[max_index - number_of_tickets:max_index])
            return conver_to_Ticket_class(tickets[min_index:max_index])
    else:
        return conver_to_Ticket_class(tickets[:number_of_tickets] if len(tickets) > number_of_tickets else tickets)


def get_hotel(location, check_in, check_out, budget=None, min_stars=0, number_of_hotels=1) -> list[Hotel]:
    """
    Fetches the hotel based on the specified parameters.

    Parameters:
    :param location: str, Name of the location (can use IATA code).
    :param check_in: str, Check-in date (format YYYY-MM-DD).
    :param check_out: str, Check-out date (format YYYY-MM-DD).
    :param budget: float, optional, Maximum price for the hotel.
    :param min_stars: min number of stars for hotel required
    :param number_of_hotels: number of different hotels to return

    :return: list of 'Hotel' class
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
    if budget and (not budget == "None"):
        # Initialize the last index of the ticket list to include
        last_index = 0
        # Iterate through the tickets to find those within budget
        for i, hotel in enumerate(hotels):
            if hotel['priceFrom'] < budget:
                last_index = i
            else:
                break
        # Slice the tickets list to only include tickets within budget
        if len(hotels) <= number_of_hotels:
            return conver_to_Hotel_class(hotels)
        else:
            min_index = max(0, last_index - (number_of_hotels // 2))
            max_index = min(len(hotels), last_index + (number_of_hotels // 2) + (number_of_hotels % 2))
            if max_index - min_index < number_of_hotels:
                if min_index == 0:
                    return conver_to_Hotel_class(hotels[:number_of_hotels])
                else:
                    return conver_to_Hotel_class(hotels[max_index - number_of_hotels:max_index])
            return conver_to_Hotel_class(hotels[min_index:max_index])
    else:
        return conver_to_Hotel_class(hotels[:number_of_hotels] if len(hotels) > number_of_hotels else hotels)


def find_top_routes(origin, destination, departure_at=None, return_at=None, budget=None, route_number=3, min_stars=0,
                    max_transfers=0, airlines=(), max_flight_duration=None) -> \
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
    :param max_transfers: max number of transfers during a flight, 0 by default
    :param airlines: list of airlines which are required for a flight, by default empty tuple - all airlines are allowed
    :param max_flight_duration: max duration of a flight in hours, None by default

    :return: list of 'Route' class
    """
    # Get the cheapest ticket and hotel
    cheapest_ticket = get_ticket(origin=origin, destination=destination, departure_at=departure_at,
                                 return_at=return_at, max_transfers=max_transfers, airlines=airlines,
                                 max_flight_duration=max_flight_duration)[0]
    cheapest_hotel = get_hotel(location=destination, check_in=departure_at, check_out=return_at, min_stars=min_stars)[0]

    # Create a return array with the initial cheapest route
    top_routes = [{
        'ticket': cheapest_ticket,
        'hotel': cheapest_hotel
    }]

    # Define minimum prices
    min_ticket_price = cheapest_ticket.ticket_price
    min_hotel_price = cheapest_hotel.hotel_price_from

    # Check if budget is specified
    if budget and (not budget == "None"):
        # Check if the cheapest route exceeds the budget
        if cheapest_hotel.hotel_price_from + cheapest_ticket.ticket_price > budget:
            # cheapest route exceed the budget, return the cheapest route
            return [Route(origin=origin, destination=destination, departure_at=departure_at, return_at=return_at,
                          budget=budget, ticket=top_routes[0]['ticket'], hotel=top_routes[0]['hotel'])]
        else:
            # Make return value empty
            top_routes = []
            # Define part of a budget for tickets
            coef = min_ticket_price / (min_ticket_price + min_hotel_price)
            ticket_price = max(coef * budget * 0.9, min_ticket_price)
            # get ticket list
            tickets = get_ticket(origin=origin, destination=destination, departure_at=departure_at,
                                 return_at=return_at, budget=ticket_price, number_of_tickets=route_number,
                                 max_transfers=max_transfers, airlines=airlines,
                                 max_flight_duration=max_flight_duration)

            # define budget for a hotel
            hotel_price = budget - tickets[len(tickets) // 2].ticket_price
            # get hotel list
            hotels = get_hotel(location=destination, check_in=departure_at, check_out=return_at,
                               budget=hotel_price, min_stars=min_stars, number_of_hotels=route_number)
            # check sizing
            if len(hotels) != len(tickets):
                # make size of arrays equal
                if len(hotels) < len(tickets):
                    while len(hotels) < len(tickets):
                        hotels.append(hotels[-1])
                else:
                    while len(tickets) < len(hotels):
                        tickets.append(tickets[-1])

            # combine top routes
            for i in range(len(tickets)):
                top_routes.append({
                    'ticket': tickets[i],
                    'hotel': hotels[len(tickets) - 1 - i]
                })
    else:
        # Budget is not specified, finding arbitrary routes
        for _ in range(1, route_number):
            min_ticket_price *= 2
            ticket = get_ticket(origin=origin, destination=destination, departure_at=departure_at,
                                return_at=return_at, budget=min_ticket_price, max_transfers=max_transfers,
                                airlines=airlines,
                                max_flight_duration=max_flight_duration)[0]
            min_hotel_price *= 3
            hotel = get_hotel(location=destination, check_in=departure_at, check_out=return_at,
                              budget=min_hotel_price, min_stars=min_stars)[0]
            top_routes.append({
                'ticket': ticket,
                'hotel': hotel
            })

    # Remove duplicates and convert to Route class
    unique_routes = []
    for i in range(len(top_routes)):
        if i == 0 or (top_routes[i]['ticket'].ticket != top_routes[i - 1]['ticket'].ticket or top_routes[i]['hotel'].hotel !=
                      top_routes[i - 1]['hotel'].hotel):
            unique_routes.append(
                Route(origin=origin, destination=destination, departure_at=departure_at, return_at=return_at,
                      budget=budget, ticket=top_routes[i]['ticket'], hotel=top_routes[i]['hotel']))

    # collect hotel_photos
    save_hotel_photo_urls(unique_routes)

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
    file_path = data_directory_path() + hotel_api.hotels_list_dir + f'/{locationId}.json'
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

def conver_to_Ticket_class(tickets) -> list[Ticket]:
    """
    This function converts list of tickets json type to list of tickets of class 'Ticket'
    :param tickets: list of tickets of json type
    :return: list of tickets of class 'Ticket'
    """
    return [Ticket(ticket=ticket) for ticket in tickets]

def conver_to_Hotel_class(hotels) -> list[Hotel]:
    """
    This function converts list of tickets json type to list of tickets of class 'Hotel'
    :param hotels: list of hotels of json type
    :return: list of hotels of class 'Hotel'
    """
    return [Hotel(hotel) for hotel in hotels]

def save_hotel_photo_urls(routes: list[Route]):
    """
    This function saves photos from hotels from route
    :param routes: list of routes
    :return:
    """
    # collect photo ids
    hotel_ids = [route.hotel.hotel_id for route in routes]

    # save photos
    hotel_api = HotelApi()
    urls_list = hotel_api.fetch_hotel_photos(hotel_ids=hotel_ids, return_only_urls=True)
    for route in routes:
        for photo_id in urls_list[str(route.hotel.hotel_id)]:
            route.hotel.photo_urls.append(f'https://photo.hotellook.com/image_v2/limit/{photo_id}/800/520.auto')
