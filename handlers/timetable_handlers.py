from config import bot
from Misc.message import Message
from Misc.states import States
from DB_Helper.SQLHelper import SQLHelper
from DB_Helper.RedisHelper import set_state, get_current_state, get_message
from Serega.ToTheMain import BackToMain
from Serega.Timetable import GetTodayDate, GetTimetable
from .markups import day_choose_markup as m
import logging

timetable_logger = logging.getLogger('Bot.timetable_handle')

day_to_number = {
    'понедельник':0,
    'вторник':1,
    'среда':2,
    'четверг':3,
    'пятница':4,
    'суббота':5
}

#Обработка расписания
@bot.message_handler(func = lambda message: get_current_state(message.chat.id) == States.S_NORMAL.value and message.text.lower() == "расписание")
def choose_dey(message):
    chat_id = message.chat.id
    
    timetable_logger.error("User %s wrote a command" % chat_id)

    db_worker = SQLHelper()
    user_type = db_worker.TakeInfo(chat_id)[1]
    db_worker.close()

    #Если пользователь не абитуриент, то выводим календарь
    if user_type != "abiturient":
        timetable_logger.error("User %s got a timetable keyboard" % chat_id)
        date = GetTodayDate(0)
        set_state(chat_id, States.S_TIMETABLE.value)
        bot.send_message(chat_id=chat_id,
                        text= get_message(Message.M_TimeTable_Today.value).format(date),
                        reply_markup=m.day_choose_kb)

@bot.message_handler(func = lambda message: get_current_state(message.chat.id) == States.S_TIMETABLE.value)
def send_timetable(message):
    chat_id = message.chat.id
    text = message.text.lower()

    #Если выбран день недели
    if text in day_to_number:
        #Получаем группу пользователя
        db_worker = SQLHelper()
        group = db_worker.TakeInfo(chat_id)[2]
        db_worker.close()

        res = GetTimetable(group, day_to_number[text])
        
        bot.send_message(chat_id=chat_id, text= res)

        timetable_logger.error("User %s got a timetable" % chat_id)

        BackToMain(chat_id, "Главное меню")
        
    #Авторасписание
    elif text == 'авторасписание':
        timetable_logger.error("User %s changed auto timetable parameter" % chat_id)

        db_worker = SQLHelper()
        BackToMain(chat_id, (db_worker.UpdateAuto(chat_id)))
        db_worker.close()

    #Назад
    elif text == 'назад':
        timetable_logger.error("User %s returned to the main menu" % chat_id)

        BackToMain(chat_id, get_message(Message.M_MainMenu.value))

    #Ничего из предложенного
    else:
        timetable_logger.error("User %s made wrong choice: %s" % (chat_id, text))
        bot.send_message(chat_id = chat_id,
                        text= get_message(Message.M_Error_Wrong_Choice))