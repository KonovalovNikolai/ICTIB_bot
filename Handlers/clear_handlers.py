import logging

from Serega.User_Class import User

from Misc import M, B, S
from .Markups import yes_no_kb
from telebot import types
from config import bot

clear_logger = logging.getLogger('Bot.clear_handle')

#Обработка команды "clear"
@bot.message_handler(commands = ['clear'],
                    func = lambda message: User(message).GetUserState() == S.NORMAL)
def ClearComand(message):
    """
    Rоманда удаления пользователя из базы данных
    В основном нужна для отладки
    Только из основного состояния
    """
    user = User(message, bot)
    user.SendMessage(text=M.CLEAR_СONFIRMATION,
                    reply_markup=yes_no_kb,
                    state=S.CLEAR)

    clear_logger.error("Пользователь %s получил клавиатуру для потверждения удаления" % message.chat.id)

#Обработка подверждения
@bot.message_handler(func = lambda message: User(message).GetUserState() == S.CLEAR)
def user_entering_type(message):
    """
    Обработка клавиатуры для потверждения удаления
    Только из состояния удаления
    """
    user = User(message, bot)
    text = message.text

    if (text == B.YES):
        user.DeleteUser()
        user.SendMessage(text=M.CLEAR_BYE,
                        reply_markup = types.ReplyKeyboardRemove())

        clear_logger.error("Пользователь %s потвердил удаление" % message.chat.id)
    
    elif (text == B.NO):
        user.BackToMain(M.CLEAR_CANCEL)

        clear_logger.error("Пользователь %s отменил удаление" % message.chat.id)
    
    else:
        user.SendMessage(text = M.ERROR_WRONG_CHOICE)

        clear_logger.error("Пользователь %s сделал неправильный выбор: %s" % (message.chat.id, text))
