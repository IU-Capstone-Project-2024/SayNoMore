import telebot
import sys

from api_collector.route import route_collector
from utils import messages
from utils.formatting import request_to_json, format_route_info


class SayNoMoreBot:
    def __init__(self):
        self.bot = telebot.TeleBot('7333725090:AAFC6DwjlSs5VvvJ6ML863e5yx8h-NgAR60')
        self.second = False
        self.setup_handlers()
        self.route_collector = route_collector

    def setup_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def send_welcome(message):
            self.bot.send_message(message.chat.id, messages.WELCOME_MESSAGE)

        @self.bot.message_handler(func=lambda message: True)
        def handle_user_request(message):
            self.process_message(message)

    def run(self):
        self.bot.polling()

    def process_message(self, message):
        if message.text == 'I want to leave Kazan on July 1st.' and not self.second:
            self.bot.send_message(message.chat.id, messages.MORE_INFO_MESSAGE)
            self.second = True
        elif message.text == "I will go to Moscow. Returning on July 22nd. The budget is 800 thousand." and self.second:
            self.bot.send_message(message.chat.id, messages.AWAIT_MESSAGE)
            analyzed_message = "Arrival:2024-08-01;Return:2024-08-22;Departure:KZN;Destination:SVO;Budget:800000"
            self.second = False
            request = request_to_json(analyzed_message)
            rc = route_collector.RouteCollector()
            routes_list = rc.find_top_routes(request['Departure'],
                                             request['Destination'],
                                             request['Arrival'],
                                             request['Return'],
                                             request['Budget'])

            routes_str = format_route_info(routes_list)
            self.bot.send_message(message.chat.id, routes_str)
        else:
            self.bot.send_message(message.chat.id, 'ERROR')
            sys.exit(0)


if __name__ == "__main__":
    bot = SayNoMoreBot()
    bot.run()
