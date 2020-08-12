import telebot
from requests import ConnectionError
import time

from config import bot
from DB_Helper.RedisHelper import get_message

SLEEPTIME = 1

def Send_message(chat_id, text, raw = True, reply_to_message_id=None,
                reply_markup=None, parse_mode=None, form : list = None):
    if raw:
        text = get_message(text)
        if form:
            text = text.format(*form)
    try:
        bot.send_message(chat_id, text, reply_to_message_id = reply_to_message_id,
                        reply_markup=reply_markup, parse_mode=parse_mode)
    except ConnectionError:
        time.sleep(SLEEPTIME)
        bot.send_message(chat_id, text, reply_to_message_id = reply_to_message_id,
                        reply_markup=reply_markup, parse_mode=parse_mode)

