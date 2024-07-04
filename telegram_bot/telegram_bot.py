import telebot
import sys
import asyncio
import threading
import json
from telebot import types

from api_collector.route.route import find_top_routes
from telegram_bot.utils import messages
from telegram_bot.utils.formatting import route_list_to_string
from request_analyzer.request_analyzer import RequestAnalyzer
from request_analyzer.llm import LLM

# Global dictionary to track user states
user_states = {}

class SayNoMoreBot:
    def __init__(self):
        self.bot = telebot.TeleBot('7333725090:AAFC6DwjlSs5VvvJ6ML863e5yx8h-NgAR60')
        self.setup_handlers()

    def setup_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def send_welcome(message):
            self.bot.send_message(message.chat.id, messages.WELCOME)

        @self.bot.message_handler(commands=['help'])
        def send_help(message):
            self.bot.send_message(message.chat.id, messages.HELP)

        @self.bot.message_handler(func=lambda message: True)
        def handle_user_request(message):
            asyncio.run(self.process_message(message))

        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_query(call):
            self.handle_callback_query(call)

    def run(self):
        self.bot.polling()

    async def process_message(self, message):
        user_id = message.chat.id
        if user_id not in user_states:
            user_states[user_id] = {
                "analyzer": RequestAnalyzer(LLM()),
                "step": 0,
                "completed": False,
                "messages": [],
                "routes_list": []
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
                user_state["routes_list"] = routes_list
                self.send_routes_with_buttons(message.chat.id, routes_list)
            else:
                user_state["step"] += 1
        else:
            self.bot.send_message(message.chat.id, 'ERROR')
            sys.exit(0)

    def send_routes_with_buttons(self, chat_id, routes_list):
        markup = types.InlineKeyboardMarkup()
        for index, route in enumerate(routes_list):
            markup.add(types.InlineKeyboardButton(text=f"Route {index + 1}", callback_data=f"route_{index}"))
        
        routes_message = route_list_to_string(routes_list)
        self.bot.send_message(chat_id, routes_message, reply_markup=markup)

    def handle_callback_query(self, call):
        route_index = int(call.data.split('_')[1])
        user_id = call.message.chat.id
        user_state = user_states.get(user_id)

        if user_state:
            selected_route = user_state['routes_list'][route_index]
            # Handle the selected route, e.g., send a confirmation message or process further
            self.bot.send_message(call.message.chat.id, f"You selected route {route_index + 1}:\n{selected_route.to_string()}")

if __name__ == "__main__":
    bot = SayNoMoreBot()
    threading.Thread(target=bot.run).start()