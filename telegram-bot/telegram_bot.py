import telebot
import sys
import os
from datetime import datetime

route_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../api_collector/route'))
sys.path.insert(0, route_path)

import route_collector

bot = telebot.TeleBot('7333725090:AAFC6DwjlSs5VvvJ6ML863e5yx8h-NgAR60')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        'Hi, welcome to SayNoMore bot. Tell us more bout the trip you are planning'
    )


second = False


def request_to_json(request: str) -> dict:
    pairs = request.split(';')
    json_dict = {
        key: value
        for key, value in (pair.split(':') for pair in pairs)
    }
    json_dict['Budget'] = int(json_dict['Budget'])
    return json_dict


def format_route_info(routes):

    def format_datetime(dt_str):
        # Convert the ISO format datetime string to a more readable format
        dt = datetime.fromisoformat(dt_str)
        return dt.strftime('%Y-%m-%d %H:%M:%S')

    formatted_routes = []
    for route in routes:
        ticket = route.get('ticket', {})
        hotel = route.get('hotel', {})

        flight_number = ticket.get('flight_number', 'N/A')
        departure = format_datetime(ticket.get('departure_at', 'N/A'))
        return_date = format_datetime(ticket.get('return_at', 'N/A'))
        origin = ticket.get('origin', 'N/A')
        destination = ticket.get('destination', 'N/A')
        price = ticket.get('price', 'N/A')

        hotel_name = hotel.get('hotelName', 'N/A')
        hotel_price = hotel.get('priceFrom', 'N/A')

        formatted_route = (f"Flight:\n"
                           f"  - Flight Number: {flight_number}\n"
                           f"  - From: {origin} to {destination}\n"
                           f"  - Departure: {departure}\n"
                           f"  - Return: {return_date}\n"
                           f"  - Price: {price} RUB\n"
                           f"Hotel:\n"
                           f"  - Name: {hotel_name}\n"
                           f"  - Price: {hotel_price:.2f} RUB\n")

        formatted_routes.append(formatted_route)

    return "\n---\n".join(formatted_routes)


@bot.message_handler(func=lambda message: True)
def handle_user_request(message):
    global second
    if message.text == 'I want to leave Kazan on July 1st.' and not second:
        bot.send_message(
            message.chat.id,
            'It seems that I did not receive all the necessary information for your request. Please '
            'specify the destination city. Additionally, if you have a budget, you can provide that too, '
            'although it is not mandatory. Thank you!')
        second = True
    elif message.text == "I will go to Moscow. Returning on July 22nd. The budget is 800 thousand." and second:
        bot.send_message(message.chat.id,
                         "All good, let me prepare a trip plans for you")
        analyzed_message = "Arrival:2024-08-01;Return:2024-08-22;Departure:KZN;Destination:SVO;Budget:800000"
        second = False
        request = request_to_json(analyzed_message)
        rc = route_collector.RouteCollector()
        routes_list = rc.find_top_routes(request['Departure'],
                                         request['Destination'],
                                         request['Arrival'], request['Return'],
                                         request['Budget'])

        routes_str = format_route_info(routes_list)
        bot.send_message(message.chat.id, routes_str)
    else:
        bot.send_message(message.chat.id, 'ERROR')
        sys.exit(0)


bot.polling()
