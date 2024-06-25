import asyncio
import telebot
import sys

from request_analyzer.request_analyzer import RequestAnalyzer
from request_analyzer.llm import LLM

requests = [
    "Хочу уехать в Москву c 1го по 15 декабря",
    "Я поеду из Казани. Бюджет примерно 35 тысяч"
]
request_idx = 0
message = ""

async def analyze_requests():
    global request_idx
    request_analyzer = RequestAnalyzer(LLM())  # Ensure self.llm is defined somewhere
    while True:
        are_all_fields_retireved, message = await request_analyzer.analyzer_step(requests[request_idx])
        print(message)
        if are_all_fields_retireved:
            break                
        request_idx += 1

# Run the async function
asyncio.run(analyze_requests())
