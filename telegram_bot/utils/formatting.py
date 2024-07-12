from api_collector.route.route import Route
from google.cloud import translate_v2 as translate
import os


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


def route_list_to_string(route_list: list[Route]) -> str:
    """
    Converts a list of Route objects into a formatted string.

    Args:
        route_list (list[Route]): A list of Route objects.

    Returns:
        str: A formatted string representation of the route list.
    """
    result = ''
    for route in route_list:
        result += route.to_string()
        result += '\n________________________\n'
    return result


def translate_to_russian(text):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'telegram_bot/secrets/translationkey.json'
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language='ru')
    return result['translatedText']