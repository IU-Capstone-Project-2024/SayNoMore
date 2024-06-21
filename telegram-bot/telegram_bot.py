import telebot
import sys

bot = telebot.TeleBot('7333725090:AAFC6DwjlSs5VvvJ6ML863e5yx8h-NgAR60')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id,
                     'Hi, welcome to SayNoMore bot. Tell us more bout the trip you are planning')


second = False


@bot.message_handler(func=lambda message: True)
def handle_user_request(message):
    global second
    if message.text == 'Хочу уехать из Казани 1го декабря' and not second:
        bot.send_message(message.chat.id,
                         'Похоже, что я не получил все необходимые данные для вашего запроса. Пожалуйста, '
                         'укажите город назначения. Кроме того, если у вас есть бюджет, вы можете указать и его, '
                         'хотя это не обязательно. Спасибо!')
        second = True
    elif message.text == "Я уеду в Москву. Обратно отправляюсь 22го декабря. Бюджет 35 тысяч." and second:
        bot.send_message(message.chat.id, "All, Let be prepare several trip plans for you")
        analyzed_message = "Arrival:01/12/2024;Return:22/12/2024;Departure:Казань;Destination:Москва;Budget:35000"



