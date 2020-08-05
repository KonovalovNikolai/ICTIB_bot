import logging

from DB_Helper.RedisHelper import set_state, get_current_state, delet_user, get_message
from DB_Helper.SQLHelper import SQLHelper
from Serega.send_message import send_message
from Serega.ToTheMain import BackToMain
from Misc import message as M
from Misc import buttons as B
from Misc import states as S
from .markups import yes_no_markup as m
from telebot import types
from config import bot

clear_logger = logging.getLogger('Bot.clear_handle')

#Обработка команды "clear"
@bot.message_handler(commands = ['clear'],
                    func = lambda message: get_current_state(message.chat.id) == S.NORMAL)
def command_handler(message):
    """
    Rоманда удаления пользователя из базы данных
    В основном нужна для отладки
    Только из основного состояния
    """
    chat_id = message.chat.id

    #Отправить клавиатуру потверждения
    send_message(chat_id = chat_id,
                text = get_message(M.CLEAR_СONFIRMATION),
                reply_markup = m.yes_no_kb)

    clear_logger.error("Пользователь %s получил клавиатуру для потверждения удаления" % chat_id)

    set_state(chat_id, S.CLEAR)

#Обработка подверждения
@bot.message_handler(func = lambda message: get_current_state(message.chat.id) == S.CLEAR)
def user_entering_type(message):
    """
    Обработка клавиатуры для потверждения удаления
    Только из состояния удаления
    """
    chat_id = message.chat.id
    text = message.text

    if (text == B.YES):
        send_message(chat_id = chat_id,
                    text = get_message(M.CLEAR_BYE),
                    reply_markup = types.ReplyKeyboardRemove())

        #Удаление пользователя из sqlite
        db_worker = SQLHelper()
        db_worker.DeleteUser(chat_id)
        db_worker.close()
        #Удаление пользователя из Redis
        delet_user(chat_id)

        clear_logger.error("Пользователь %s потвердил удаление" % chat_id)
    
    elif (text == B.NO):
        BackToMain(chat_id, get_message(M.CLEAR_CANCEL))

        clear_logger.error("Пользователь %s отменил удаление" % chat_id)
    
    else:
        send_message(chat_id = chat_id,
                    text = get_message(M.ERROR_WRONG_CHOICE))

        clear_logger.error("Пользователь %s сделал неправильный выбор: %s" % (chat_id, text))
