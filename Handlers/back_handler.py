import logging

from DB_Helper.RedisHelper import get_current_state
from Serega.ToTheMain import BackToMain
from Misc import S, B
from config import bot

@bot.message_handler(func = lambda message: message.text == B.BACK
            and get_current_state(message.chat.id) >= S.NORMAL)
def go_back(message):
    chat_id = message.chat.id
    BackToMain(chat_id)