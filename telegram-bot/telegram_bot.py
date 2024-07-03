import telebot
import sys
import asyncio
import threading
import json

from api_collector.route.route import find_top_routes
from telegram_bot.utils import messages
from telegram_bot.utils.formatting import route_list_to_string
from request_analyzer.request_analyzer import RequestAnalyzer
from request_analyzer.llm import LLM

# Global dictionary to track user states
user_states = {}

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
            asyncio.run(self.process_message(message))

    def run(self):
        """
        Starts the bot polling loop.
        """
        self.bot.polling()

    async def process_message(self, message):
        user_id = message.chat.id
        if user_id not in user_states:
            user_states[user_id] = {
                "analyzer": RequestAnalyzer(LLM()),
                "step": 0,
                "completed": False,
                "messages": []
            }

        user_state = user_states[user_id]
        user_state["messages"].append(message.text)

        if not user_state["completed"]:
            are_all_fields_retrieved, response_message = await user_state["analyzer"].analyzer_step(user_state["messages"][user_state["step"]])
            self.bot.send_message(message.chat.id, response_message)
            
            if are_all_fields_retrieved:
                user_state["completed"] = True
                request = json.loads(response_message)  # Assuming this is the final analyzed message
                routes_list = find_top_routes(
                    origin=request['Departure'],
                    destination=request['Destination'],
                    departure_at=request['Arrival'],
                    return_at=request['Return'],
                    budget=request['Budget']
                )
                self.bot.send_message(message.chat.id, route_list_to_string(routes_list))
            else:
                user_state["step"] += 1
        else:
            self.bot.send_message(message.chat.id, 'ERROR')
            sys.exit(0)

if __name__ == "__main__":
    bot = SayNoMoreBot()
    threading.Thread(target=bot.run).start()
