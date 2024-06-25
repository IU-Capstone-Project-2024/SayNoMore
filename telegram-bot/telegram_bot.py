import telebot
import sys

from api_collector.route.route import Route, find_top_routes
from utils import messages
from utils.formatting import request_to_json, route_list_to_string


class SayNoMoreBot:
    """
    A Telegram bot to assist users in finding travel routes based on their requirements.

    Attributes:
        bot (TeleBot): Instance of the TeleBot.
        second (bool): Flag to track the state of user interaction.
    """

    def __init__(self):
        """
        Initializes the SayNoMoreBot instance and sets up the command handlers.
        """
        self.bot = telebot.TeleBot('7333725090:AAFC6DwjlSs5VvvJ6ML863e5yx8h-NgAR60')
        self.second = False
        self.setup_handlers()

    def setup_handlers(self):
        """
        Sets up the command handlers for the bot.
        """

        @self.bot.message_handler(commands=['start'])
        def send_welcome(message):
            """
            Sends a welcome message to the user when the /start command is received.

            Args:
                message (Message): The message object containing user information.
            """
            self.bot.send_message(message.chat.id, messages.WELCOME)

        @self.bot.message_handler(commands=['help'])
        def send_help(message):
            """
            Sends a help message to the user when the /help command is received.

            Args:
                message (Message): The message object containing user information.
            """
            self.bot.send_message(message.chat.id, messages.HELP)

        @self.bot.message_handler(func=lambda message: True)
        def handle_user_request(message):
            """
            Handles any user message and processes it.

            Args:
                message (Message): The message object containing user information.
            """
            self.process_message(message)

    def run(self):
        """
        Starts the bot polling loop.
        """
        self.bot.polling()

    def process_message(self, message):
        """
        Processes the user message and provides appropriate responses based on the interaction state.

        Args:
            message (Message): The message object containing user information.
        """
        if message.text == 'I want to leave Kazan on July 1st.' and not self.second:
            self.bot.send_message(message.chat.id, messages.MORE_INFO)
            self.second = True
        elif message.text == "I will go to Moscow. Returning on July 22nd. The budget is 800 thousand." and self.second:
            self.bot.send_message(message.chat.id, messages.AWAIT)
            analyzed_message = "Arrival:2024-08-01;Return:2024-08-22;Departure:KZN;Destination:SVO;Budget:800000"
            self.second = False
            request = request_to_json(analyzed_message)
            routes_list = find_top_routes(
                origin=request['Departure'],
                destination=request['Destination'],
                departure_at=request['Arrival'],
                return_at=request['Return'],
                budget=request['Budget']
            )
            self.bot.send_message(message.chat.id, route_list_to_string(routes_list))
        else:
            self.bot.send_message(message.chat.id, 'ERROR')
            sys.exit(0)


if __name__ == "__main__":
    bot = SayNoMoreBot()
    bot.run()