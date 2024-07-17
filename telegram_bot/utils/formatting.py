from google.cloud import translate_v2 as translate
from deep_translator import GoogleTranslator
import os
import pandas as pd
from datetime import datetime


def request_to_json(request: str) -> dict:
    """
    Converts a request string into a dictionary with appropriate key-value pairs.

    Args:
        request (str): The request string in the format "key1:value1;key2:value2;...".

    Returns:
        dict: A dictionary representation of the request, with 'Budget' converted to an integer.
    """
    pairs = request.split(';')
    json_dict = {key: value for key, value in (pair.split(':') for pair in pairs)}
    json_dict['Budget'] = int(json_dict['Budget'])
    return json_dict


def route_list_to_string(route_list, language) -> str:
    """
    Converts a list of Route objects into a formatted string.

    Args:
        route_list (list[Route]): A list of Route objects.

    Returns:
        str: A formatted string representation of the route list.
    """
    result = ''
    for route in route_list:
        if language == "en":
            result += route.to_string_en()
        else:
            result += route.to_string_ru()
        result += '\n________________________\n'
    return result


def translate_to_russian_old(text):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'telegram_bot/secrets/translationkey.json'
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language='ru')
    return result['translatedText']

def translate_to_russian(text):
    translator = GoogleTranslator(source='en', target='ru')
    translation = translator.translate(text)
    return translation

def translate_to_english(text):
    translator = GoogleTranslator(source='ru', target='en')
    translation = translator.translate(text)
    return translation

def get_iata_code(city: str):
    df = pd.read_csv('data/all_cities_codes.csv')
    city_name_to_code = dict(zip(df['city_name'], df['city_code']))
    return city_name_to_code.get(city)

def format_web_app_data(data):
        request = {}
        request['Arrival'] = datetime.strptime(data['arrival'], "%Y-%m-%d").strftime("%Y-%m-%d")
        request['Return'] = datetime.strptime(data['return'], "%Y-%m-%d").strftime("%Y-%m-%d")
        request['Departure'] = get_iata_code(data['departure'])
        request['Destination'] = get_iata_code(data['destination'])
        if data['budget'] == "":
             request['Budget'] = "None"
        else:
            request['Budget'] = int(data['budget'])
        return request