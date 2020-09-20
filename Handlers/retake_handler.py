import logging

from Serega.User_Class import User
from Misc import S, B, M
from config import bot

@bot.message_handler(func = lambda message: message.text == B.RETAKE and
                    User(message).GetUserState() >= S.NORMAL)
def Send_Retake(message):
    user = User(message, bot)
    user.SendMessage(text=M.RETAKE)