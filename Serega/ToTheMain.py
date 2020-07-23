import logging
from handlers.markups import main_markup as m
from config import bot
from Misc.states import States
from DB_Helper.SQLHelper import SQLHelper
from DB_Helper.RedisHelper import set_state, get_current_state

logger = logging.getLogger('Bot.ToTheMain')

def BackToMain(chat_id, text):
    db_worker = SQLHelper()
    user_type = db_worker.TakeInfo(chat_id)[1]

    set_state(chat_id, States.S_NORMAL.value)

    if user_type == "stud":
        bot.send_message(chat_id= chat_id,
                        text= text,
                        reply_markup=m.main_markup_stud_kb)
        logger.error("User %s was returned to the main menu as student" % chat_id)
    elif user_type == "teach":
        bot.send_message(chat_id= chat_id,
                        text= text,
                        reply_markup=m.main_markup_teach_kb)
        logger.error("User %s was returned to the main menu as teacher" % chat_id)
    elif user_type == "abiturient":
        bot.send_message(chat_id= chat_id,
                        text= text,
                        reply_markup=m.main_markup_abiturient_kb)
        logger.error("User %s was returned to the main menu as abiturient" % chat_id)
    db_worker.close()