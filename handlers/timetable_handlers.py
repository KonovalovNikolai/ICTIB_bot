import logging

from DB_Helper.RedisHelper import set_state, get_current_state, get_message
from DB_Helper.SQLHelper import SQLHelper
from Serega.send_message import send_message
from Serega.Timetable import GetTodayDate, GetTimetable
from Serega.ToTheMain import BackToMain
from Misc import message as M
from Misc import buttons as B
from Misc import states as S
from Misc import users as U
from .Markups import day_choose_kb
from config import bot

timetable_logger = logging.getLogger('Bot.timetable_handle')

#Словарь для перевода дней недели в числа
day_to_number = {
    'понедельник':0,
    'вторник':1,
    'среда':2,
    'четверг':3,
    'пятница':4,
    'суббота':5
}

#Обработка нажатия кнопки "расписание"
@bot.message_handler(func = lambda message: get_current_state(message.chat.id) == S.NORMAL
                        and message.text == B.MAIN_MENU_TTABLE)
def choose_day(message):
    """
    Только из начального состояния.
    После нажатия кнопки проверяем тип пользователя.
    Если он не абитуриен, то выводим клавиатуры для выбора дня.
    """
    chat_id = message.chat.id
    
    timetable_logger.error("Пользователь %s нажал на кнопку 'расписание'." % chat_id)

    #Определяем тип пользователя
    db_worker = SQLHelper()
    user_type = db_worker.TakeInfo(chat_id)[1]
    db_worker.close()

    #Если пользователь не абитуриент, то выводим календарь
    if (user_type != U.ABITUR):
        date = GetTodayDate(0) #Сегоднящняя дата
        send_message(chat_id=chat_id,
                        text= get_message(M.TIMETABLE_TODAY).format(date),
                        reply_markup=day_choose_kb)
        
        timetable_logger.error("Пользователь %s получил клавиатуру расписания" % chat_id)

        #Меняем тип пользователя
        set_state(chat_id, S.TIMETABLE)

#Обработка клавиатуры расписания
@bot.message_handler(func = lambda message: get_current_state(message.chat.id) == S.TIMETABLE)
def send_timetable(message):
    """
    Хэндлер для обработки клавиатуры расписания
    Только из состояния получения расписания
    """
    chat_id = message.chat.id
    text = message.text.lower()

    #Если выбран день недели
    if (text in day_to_number):
        #Получаем группу пользователя
        db_worker = SQLHelper()
        group = db_worker.TakeInfo(chat_id)[2]
        db_worker.close()

        #Получаем расписание
        res = GetTimetable(group, day_to_number[text])
        #Вывод расписания
        send_message(chat_id=chat_id, text= res)

        timetable_logger.error("Пользователь %s получил расписаниеч" % chat_id)
        
        #Возвращение в меню
        BackToMain(chat_id)
        
    #Авторасписание
    elif (text == B.AUTO_TABLE.lower()):
        #Меняем параметр авторасписания в бд
        db_worker = SQLHelper()
        ret = db_worker.UpdateAuto(chat_id)
        db_worker.close()

        send_message(chat_id= chat_id,
                    text= ret)
        BackToMain(chat_id)

        timetable_logger.error("Пользователь %s изменил параметр авторасписания:\n\t%s" % (chat_id, ret))

    #Ничего из предложенного
    else:
        timetable_logger.error("Пользователь %s сделал неправильный выбор: %s" % (chat_id, text))
        send_message(chat_id = chat_id,
                    text= get_message(M.ERROR_WRONG_CHOICE))
