from DB_Helper.RedisHelper import set_state, get_current_state
from DB_Helper.SQLHelper import SQLHelper
from handlers.Markups import main_markup_abiturient_kb, main_markup_stud_kb, main_markup_teach_kb
from Misc import S, U
from config import bot
import logging

logger = logging.getLogger('Bot.ToTheMain')

def BackToMain(chat_id, text = "🏠 Главное меню."):
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
        bot.send_message(chat_id= chat_id,
                        text= text,
                        reply_markup=main_markup_stud_kb)

        logger.error("Пользователь %s вернулся в главное меню как студент" % chat_id)

    elif user_type == U.TEACH:
        bot.send_message(chat_id= chat_id,
                        text= text,
                        reply_markup=main_markup_teach_kb)
        logger.error("Пользователь %s вернулся в главное меню как препод" % chat_id)

    elif user_type == U.ABITUR:
        bot.send_message(chat_id= chat_id,
                        text= text,
                        reply_markup=main_markup_abiturient_kb)
        logger.error("Пользователь %s вернулся в главное меню как абитуриент" % chat_id)
    
    #Меняем состояние пользователя
    set_state(chat_id, S.NORMAL)