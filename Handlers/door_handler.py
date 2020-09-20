import logging

from Serega.User_Class import User
from Misc import S, B, M
from config import bot

@bot.message_handler(func = lambda message: message.text == B.DOORS and
                    User(message).GetUserState() == S.NORMAL)
def send_doors(message):
    User(message, bot).SendMessage(text=M.DOORS)