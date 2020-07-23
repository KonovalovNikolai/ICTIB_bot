import logging
from config import bot
from Misc.states import States
from Misc.message import Message
from DB_Helper.SQLHelper import SQLHelper
from DB_Helper.RedisHelper import set_state, get_current_state, delet_user, get_message
from telebot import types
from .markups import yes_no_markup as m
from Serega.ToTheMain import BackToMain

clear_logger = logging.getLogger('Bot.clear_handle')

#команда удаления пользователя из базы данных
#в основном нужна для отладки

#обработчик команды
#Только из основного состояния
@bot.message_handler(commands = ['clear'],
                    func = lambda message: get_current_state(message.chat.id) == States.S_NORMAL.value)
def command_handler(message):
    chat_id = message.chat.id

    clear_logger.error("User %s wrote command" % chat_id)

    #Отправить клавиатуру потверждения
    bot.send_message(chat_id=chat_id,
                    text=get_message(Message.M_Clear_Сonfirmation.value),
                    reply_markup=m.yes_no_kb)

    clear_logger.error("User %s got a keyboard" % chat_id)

    set_state(chat_id, States.S_CLEAR.value)

#Обработка подверждения
@bot.message_handler(func = lambda message: get_current_state(message.chat.id) == States.S_CLEAR.value)
def user_entering_type(message):
    chat_id = message.chat.id
    text = message.text.lower()
    if text == "да":

        clear_logger.error("User %s agreed to delete info" % chat_id)

        db_worker = SQLHelper()
        db_worker.DeleteUser(chat_id)
        
        bot.send_message(chat_id=chat_id,
                        text=get_message(Message.M_Clear_Bye.value),
                        reply_markup=types.ReplyKeyboardRemove())
        
        db_worker.close()

        delet_user(chat_id)
    
    elif text == "нет":
        clear_logger.error("User %s disagreed to delete info" % chat_id)

        BackToMain(chat_id, get_message(Message.M_Clear_Cancel.value))
    
    else:
        clear_logger.error("User %s made wrong choice: %s" % (chat_id, text))

        bot.send_message(chat_id=chat_id,
                        text= get_message(Message.M_Error_Wrong_Choice.value))
