import sys
import json
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice, InputMediaPhoto, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, PreCheckoutQueryHandler, filters, ContextTypes
from api_collector.route.route import find_top_routes
from telegram_bot.utils import messages
from telegram_bot.utils.formatting import route_list_to_string, translate_to_russian
from request_analyzer.request_analyzer import RequestAnalyzer
from request_analyzer.llm import LLM

# Global dictionary to track user states
user_states = {}

class SayNoMoreBot:
    def __init__(self, token):
        self.application = Application.builder().token(token).build()
        self.setup_handlers()

    def setup_handlers(self):
        self.application.add_handler(CommandHandler("start", self.send_welcome))
        self.application.add_handler(CommandHandler("help", self.send_help))
        self.application.add_handler(CommandHandler("restart", self.restart_trip_planning))
        self.application.add_handler(CommandHandler("language", self.choose_language))
        self.application.add_handler(CommandHandler("trip_form", self.send_trip_form))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_user_request))
        self.application.add_handler(CallbackQueryHandler(self.handle_callback_query))
        self.application.add_handler(PreCheckoutQueryHandler(self.checkout))
        self.application.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, self.got_payment))

    def run(self):
        self.application.run_polling()

    async def send_welcome(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.message.chat.id
        if user_id not in user_states:
            user_states[user_id] = self.initialize_user_state()
        language = user_states[user_id]["language"]
        if language == "en":
            await update.message.reply_text(messages.WELCOME_EN)
        else:
            await update.message.reply_text(messages.WELCOME_RU)

    async def send_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.message.chat.id
        if user_id not in user_states:
            user_states[user_id] = self.initialize_user_state()
        language = user_states[user_id]["language"]
        if language == "en":
            await update.message.reply_text(messages.HELP_EN)
        else:
            await update.message.reply_text(messages.HELP_RU)

    async def restart_trip_planning(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.restart_trip_planning_sequence(update.message.chat.id)
        user_id = update.message.chat.id
        language = user_states[user_id]["language"]
        if language == "en":
            await update.message.reply_text("Trip planning sequence has been restarted. Please start again by providing your trip details.")
        else:
            await update.message.reply_text("Последовательность планирования поездки была перезапущена. Пожалуйста, начните сначала, предоставив детали вашей поездки.")

    async def choose_language(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await self.send_language_options(update.message.chat.id)

    async def send_trip_form(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await self.launch_mini_app(update.message.chat.id)

    async def handle_user_request(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.web_app_data:
            await self.handle_web_app_data(update.message)
        else:
            await self.process_message(update.message)

    async def handle_callback_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        call = update.callback_query
        user_id = call.message.chat.id
        user_state = user_states.get(user_id)
        if call.data.startswith("route_"):
            route_index = int(call.data.split('_')[1])
            user_id = call.message.chat.id
            user_state = user_states.get(user_id)
            if user_state:
                selected_route = user_state['routes_list'][route_index]
                user_state['selected_route'] = selected_route
                await call.message.reply_text(f"You selected route {route_index + 1}:\n{selected_route.to_string()}")
                await self.send_photos(user_id, selected_route.hotel.photo_urls, context)
                await self.send_payment_button(call.message.chat.id, context)
        elif call.data.startswith("lang_"):
            self.set_user_language(call.message.chat.id, call.data.split('_')[1])
            await call.message.reply_text("Language preference updated.")
        elif call.data.startswith("pay_"):
            await self.send_invoice(call.message.chat.id, context)

    async def checkout(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.pre_checkout_query
        await context.bot.answer_pre_checkout_query(pre_checkout_query_id=query.id, ok=True, error_message="Payment failed, please try again later.")

    async def got_payment(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Thank you for your payment!")

    async def launch_mini_app(self, chat_id):
        mini_app_url = f"https://iu-capstone-project-2024.github.io/SayNoMore/form?chatId={chat_id}"
        markup = InlineKeyboardMarkup([[InlineKeyboardButton(text="Open Trip Form", web_app=WebAppInfo(url=mini_app_url))]])
        await self.application.bot.send_message(chat_id, "Please fill out your trip details using the form below:", reply_markup=markup)

    async def handle_web_app_data(self, message):
        try:
            data = json.loads(message.web_app_data.data)
            chat_id = data['chatId']
            response_message = json.dumps(data, indent=4)
            await self.application.bot.send_message(chat_id, f"Received trip details:\n{response_message}")
        except Exception as e:
            await self.application.bot.send_message(message.chat.id, f"Error processing data: {e}")

    async def process_message(self, message):
        user_id = message.chat.id
        if user_id not in user_states:
            user_states[user_id] = self.initialize_user_state()

        user_state = user_states[user_id]
        user_state["messages"].append(message.text)

        if not user_state["completed"]:
            language = user_state["language"]
            if language == "en":
                translated_message = translate_to_russian(user_state["messages"][user_state["step"]])
            else:
                translated_message = user_state["messages"][user_state["step"]]

            are_all_fields_retrieved, response_message = await user_state["analyzer"].analyzer_step(translated_message)
            await self.application.bot.send_message(message.chat.id, response_message)
            
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
                await self.send_routes_with_buttons(message.chat.id, routes_list)
            else:
                user_state["step"] += 1
        else:
            await self.application.bot.send_message(message.chat.id, 'ERROR')
            sys.exit(0)

    async def send_routes_with_buttons(self, chat_id, routes_list):
        markup = InlineKeyboardMarkup([[InlineKeyboardButton(text=f"Route {index + 1}", callback_data=f"route_{index}") for index, route in enumerate(routes_list)]])
        routes_message = route_list_to_string(routes_list)
        await self.application.bot.send_message(chat_id, routes_message, reply_markup=markup)

    async def send_photos(self, chat_id, photos, context):
        if len(photos) > 5:
            photos = photos[:5]
        media_group = [InputMediaPhoto(media=photo_url) for photo_url in photos]
        await context.bot.send_media_group(chat_id, media_group)

    async def send_payment_button(self, chat_id, context):
        markup = InlineKeyboardMarkup([[InlineKeyboardButton(text="Pay", callback_data="pay_")]])
        await context.bot.send_message(chat_id, "Click to proceed with payment", reply_markup=markup)

    async def send_invoice(self, chat_id, context):
        user_state = user_states.get(chat_id)
        prices = [LabeledPrice(label='Trip Payment', amount=user_state['selected_route'].calculate_total_cost() * 100)]

        await context.bot.send_invoice(
            chat_id,
            title='Trip Payment',
            description='Payment for selected trip route',
            payload='trip-payment-payload',
            provider_token='1744374395:TEST:045d3bca5efb8ecdb8e0',
            currency='RUB',
            prices=prices,
            start_parameter='trip-payment'
        )

    async def send_language_options(self, chat_id):
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton(text="Русский", callback_data="lang_ru"), InlineKeyboardButton(text="English", callback_data="lang_en")]
        ])
        await self.application.bot.send_message(chat_id, "Choose your language / Выберите язык:", reply_markup=markup)

    def set_user_language(self, chat_id, language):
        if chat_id not in user_states:
            user_states[chat_id] = self.initialize_user_state()
        user_states[chat_id]["language"] = language

    def restart_trip_planning_sequence(self, chat_id):
        if chat_id in user_states:
            del user_states[chat_id]

    def initialize_user_state(self):
        return {
            "analyzer": RequestAnalyzer(LLM()),
            "step": 0,
            "completed": False,
            "messages": [],
            "routes_list": [],
            "language": "ru"  # Default language is Russian
        }

if __name__ == "__main__":
    bot = SayNoMoreBot('7333725090:AAFC6DwjlSs5VvvJ6ML863e5yx8h-NgAR60')
    bot.run()