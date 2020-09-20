import logging

from Serega.User_Class import User
from Misc import S, B, M
from config import bot

@bot.message_handler(func = lambda message: message.text == B.DIRECTION and
                    User(message).GetUserState() == S.NORMAL)
def send_doors(message):
    User(message, bot).SendMessage(text='http://abit.ictis.sfedu.ru/bachelor.html#directions', raw=False)