from DB_Helper.RedisHelper import set_state, get_current_state
from DB_Helper.SQLHelper import SQLHelper
from handlers.Markups import main_markup_abiturient_kb, main_markup_stud_kb, main_markup_teach_kb
from .Send_message import Send_message
from Misc import S, U, M
from config import bot
import logging

logger = logging.getLogger('Bot.ToTheMain')

def BackToMain(chat_id, text = M.MAINMENU):
    """
    Функция для возврата пользователя в главное меню учитывая его тип.
    chat_id - id пользователя.
    text - текст сообщения для отправки.
    по умолчанию выводит "🏠 Главное меню."
    """
    #Берём из бд тип пользователя
    db_worker = SQLHelper()
    user_type = db_worker.TakeInfo(chat_id)[1]
    db_worker.close()
    
    #Отправляем текст сообщения
    if user_type == U.STUDENT:
        Send_message(chat_id= chat_id,
                        text= text,
                        reply_markup=main_markup_stud_kb)

        logger.error("Пользователь %s вернулся в главное меню как студент" % chat_id)

    elif user_type == U.TEACH:
        Send_message(chat_id= chat_id,
                        text= text,
                        reply_markup=main_markup_teach_kb)
        logger.error("Пользователь %s вернулся в главное меню как препод" % chat_id)

    elif user_type == U.ABITUR:
        Send_message(chat_id= chat_id,
                        text= text,
                        reply_markup=main_markup_abiturient_kb)
        logger.error("Пользователь %s вернулся в главное меню как абитуриент" % chat_id)
    
    #Меняем состояние пользователя
    set_state(chat_id, S.NORMAL)