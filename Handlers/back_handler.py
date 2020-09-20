import logging

from Serega.User_Class import User
from Misc import S, B
from config import bot

@bot.message_handler(func = lambda message: message.text == B.BACK
            and User(message).GetUserState() >= S.NORMAL)
def BackToMainMenu(message):
    '''Обработка кнопки НАЗАД.
    Любая таккая кнопка обрабатывается только здесь'''
    user = User(message, bot)
    user.BackToMain() # возвращение пользователя в главное меню