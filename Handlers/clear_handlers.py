import logging

from Serega.User_Class import User

from Misc import M, B, S
from .Markups import yes_no_kb
from telebot import types
from config import bot

logger = logging.getLogger('Bot.ClearHandle')

@bot.message_handler(commands = ['clear'],
                    func = lambda message: User(message).GetUserState() == S.NORMAL)
def send_confirm_kb(message):
    """
    Обработка команды clear
    Команда удаления пользователя из базы данных
    В основном нужна для отладки
    Только из основного состояния
    """
    user = User(message, bot)
    # отправка клавиатуры потверждения
    user.SendMessage(text=M.CLEAR_СONFIRMATION,
                    reply_markup=yes_no_kb,
                    state=S.CLEAR)

    logger.error(f"User {user.id} got deletion confirmation button.")

#Обработка подверждения
@bot.message_handler(func = lambda message: User(message).GetUserState() == S.CLEAR)
def confirming(message):
    """
    Обработка клавиатуры для потверждения удаления
    Только из состояния удаления
    """
    user = User(message, bot)
    text = message.text

    if (text == B.YES):
        # пользователь нажал "да"
        user.DeleteUser()
        # прощание и удаление клавиатуры
        user.SendMessage(text=M.CLEAR_BYE,
                        reply_markup = types.ReplyKeyboardRemove())
        logger.error(f"User {user.id} confirmed deletion.")

    elif (text == B.NO):
        user.BackToMain(M.CLEAR_CANCEL)
        logger.error(f"User {user.id} canceled deletion.")

    else:
        user.SendMessage(text = M.ERROR_WRONG_CHOICE)
        logger.error(f"User {user.id} made wrong choice: {message.text}.")
