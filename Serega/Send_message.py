import telebot
from requests import ConnectionError
import time

from config import bot

def Send_message(chat_id, text, reply_to_message_id=None,
                reply_markup=None, parse_mode=None):
    try:
        bot.send_message(chat_id, text, reply_to_message_id = reply_to_message_id,
                        reply_markup=reply_markup, parse_mode=parse_mode)
    except ConnectionError:
        time.sleep(3)
        bot.send_message(chat_id, text, reply_to_message_id = reply_to_message_id,
                        reply_markup=reply_markup, parse_mode=parse_mode)

