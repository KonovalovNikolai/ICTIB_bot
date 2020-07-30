from DB_Helper.RedisHelper import set_state, get_current_state
from DB_Helper.SQLHelper import SQLHelper
from handlers.markups import main_markup as m
from Serega.send_message import send_message
from Misc import states as S
from Misc import users as U
import logging

logger = logging.getLogger('Bot.ToTheMain')

def BackToMain(chat_id, text = "\U0001f3e0 Главное меню."):
    """
    Функция для возврата пользователя в главное меню учитывая его тип.
    chat_id - id пользователя
    text - текст сообщения для отправки
        по умолчанию выводит "\U0001f3e0 Главное меню."
        \U0001f3e0 - юникод эмоута дома (https://unicode.org/emoji/charts/full-emoji-list.html#1f3e0)
    """
    #Берём из бд тип пользователя
    db_worker = SQLHelper()
    user_type = db_worker.TakeInfo(chat_id)[1]
    db_worker.close()
    
    #Отправляем текст сообщения
    if user_type == U.STUDENT:
        send_message(chat_id= chat_id,
                        text= text,
                        reply_markup=m.main_markup_stud_kb)

        logger.error("Пользователь %s вернулся в главное меню как студент" % chat_id)

    elif user_type == U.TEACH:
        send_message(chat_id= chat_id,
                        text= text,
                        reply_markup=m.main_markup_teach_kb)
        logger.error("Пользователь %s вернулся в главное меню как препод" % chat_id)

    elif user_type == U.ABITUR:
        send_message(chat_id= chat_id,
                        text= text,
                        reply_markup=m.main_markup_abiturient_kb)
        logger.error("Пользователь %s вернулся в главное меню как абитуриент" % chat_id)
    
    #Меняем состояние пользователя
    set_state(chat_id, S.NORMAL)