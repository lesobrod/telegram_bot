import os
import re

import requests
from telebot.types import Message
from loguru import logger
from my_redis import redis_db
from config import IMAGES_URL

# TODO X_RAPIDAPI_KEY = os.getenv('RAPID_API_KEY')

X_RAPIDAPI_KEY = "0d0b31ac33mshfdf266d3f899b69p123069jsn0ab2c41deeaa"


def exact_location(data: dict, loc_id: str) -> str:
    """
     gets the id of location and returns locations name from data

    :param data: dict Message
    :param loc_id: location id
    :return: location name
    """
    for loc in data['reply_markup']['inline_keyboard']:
        if loc[0]['callback_data'] == loc_id:
            return loc[0]['text']


def delete_tags(html_text):
    text = re.sub(r'<([^<>]*)>', '', html_text)
    return text


def request_images(loc_id: str):
    """
    Получение базы изображений отеля
    :param loc_id: String

    :return: data
    """

    querystring = {"id": loc_id}

    headers = {
        'x-rapidapi-key': X_RAPIDAPI_KEY,
        'x-rapidapi-host': "hotels4.p.rapidapi.com"
    }
    logger.info(f'Parameters for search locations: {querystring}')

    try:
        response = requests.request("GET", IMAGES_URL,
                                    headers=headers, params=querystring, timeout=20)
        data = response.json()
        logger.info(f'Hotels api(images) response received: {data}')

        if data.get('message'):
            logger.error(f'Problems with subscription to hotels api {data}')
            raise requests.exceptions.RequestException
        return data
    except requests.exceptions.RequestException as e:
        logger.error(f'Server error: {e}')
    except Exception as e:
        logger.error(f'Error: {e}')

