import logging

from Serega.User_Class import User
from config import bot

@bot.callback_query_handler(func = lambda call: True)
def End(call):
    bot.answer_callback_query(call.id)