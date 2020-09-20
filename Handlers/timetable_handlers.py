import logging

from telebot import types

from Serega.User_Class import User
from Serega.Timetable import GetTodayDate, GetTimetable
from Misc import *
from .Markups import day_choose_kb, back_kb, day_choose_search_kb
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

search = {

}

def CreateExpendKb(gp, day):
    expend_kb = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton(text = gp, callback_data= B.CALL_SEARCH_GP)
    btn2 = types.InlineKeyboardButton(text = day, callback_data= B.CALL_SEARCH_DAY)
    btn3 = types.InlineKeyboardButton(text = B.SEARCH_T, callback_data= B.CALL_SEARCH_T)
    expend_kb.add(btn1, btn2, btn3)
    return expend_kb

#Обработка нажатия кнопки "расписание"
@bot.message_handler(func = lambda message: message.text == B.MAIN_MENU_TTABLE
                        and User(message).GetUserState() == S.NORMAL)
def choose_day(message):
    """
    Только из начального состояния.
    После нажатия кнопки проверяем тип пользователя.
    Если он не абитуриен, то выводим клавиатуры для выбора дня.
    """
    user = User(message, bot)

    #Определяем тип пользователя
    user.GetUserInfo()

    #Если пользователь не абитуриент, то выводим календарь
    if (user.type != U.ABITUR):
        date = GetTodayDate(0) #Сегоднящняя дата
        user.SendMessage(text= M.TIMETABLE_TODAY,
                        form=[date],
                        reply_markup=day_choose_kb,
                        state=S.TIMETABLE)
        timetable_logger.error("Пользователь %s получил клавиатуру расписания" % message.chat.id)

#Обработка клавиатуры расписания
@bot.message_handler(func = lambda message: User(message).GetUserState() == S.TIMETABLE)
def send_timetable(message):
    """
    Хэндлер для обработки клавиатуры расписания
    Только из состояния получения расписания
    """
    user = User(message, bot)
    text = message.text.lower()

    #Если выбран день недели
    if (text in day_to_number):
        user.GetUserInfo()
        #Получаем расписание
        res = GetTimetable(name = user.group, weekday= day_to_number[text])
        #Вывод расписания
        user.SendMessage(text= res, raw=False)
        timetable_logger.error("Пользователь %s получил расписаниеч" % message.chat.id)
        user.BackToMain()

    elif (text == B.TODAY.lower()):
        user.GetUserInfo()
        #Получаем расписание
        res = GetTimetable(name = user.group, day = 0)
        #Вывод расписания
        user.SendMessage(text= res, raw=False)
        timetable_logger.error("Пользователь %s получил расписаниеч" % message.chat.id)
        user.BackToMain()

    elif (text == B.TOMORROW.lower()):
        user.GetUserInfo()
        #Получаем расписание
        res = GetTimetable(name = user.group, day = 1)
        #Вывод расписания
        user.SendMessage(text= res, raw=False)
        timetable_logger.error("Пользователь %s получил расписаниеч" % message.chat.id)
        user.BackToMain()

    elif (text == B.EXTENDED_T.lower()):
        user.GetUserInfo()
        user.SendMessage(text='Расширенный поиск расписания.\nПоиск для: {}\nДень: {}'.format(user.group, 'Сегодня'),
                        raw=False,
                        reply_markup=CreateExpendKb(user.group, 'Сегодня'))
        search[user.id] = [user.group, 'Сегодня']

    #Авторасписание
    elif (text == B.AUTO_TABLE.lower()):
        #Меняем параметр авторасписания в бд
        ret = user.UpdateAuto()
        if ret:
            answer = M.AUTO_ON
        else:
            answer = M.AUTO_OFF
        user.BackToMain(answer)
        timetable_logger.error("Пользователь %s изменил параметр авторасписания:\n\t%s" % (message.chat.id, ret))

    #Ничего из предложенного
    else:
        timetable_logger.error("Пользователь %s сделал неправильный выбор: %s" % (message.chat.id, text))
        user.SendMessage(text= M.ERROR_WRONG_CHOICE)

@bot.message_handler(func = lambda message: User(message).GetUserState() == S.SEARCH_GP)
def Set_GP(message):
    user = User(message, bot)
    if(search.get(user.id) != None):
        search[user.id][0] = message.text
    else:
        search[user.id] = [message.text, 'Сегодня']

    s = search[user.id]
    user.SendMessage(text='Расширенный поиск расписания.\nПоиск для: {}\nДень: {}'.format(*s),
                    raw=False,
                    reply_markup=CreateExpendKb(s[0], s[1]))

@bot.message_handler(func = lambda message: User(message).GetUserState() == S.SEARCH_DAY)
def Set_Day(message):
    user = User(message, bot)
    text = message.text.lower()
    if(text in day_to_number or text == B.TODAY.lower() or text == B.TOMORROW.lower()):
        if(search.get(user.id) != None):
            search[user.id][1] = message.text
        else:
            search[user.id] = ['КТбо2-6', message.text]

        s = search[user.id]
        user.SendMessage(text='Расширенный поиск расписания.\nПоиск для: {}\nДень: {}'.format(*s),
                        raw=False,
                        reply_markup=CreateExpendKb(s[0], s[1]))
    else:
        timetable_logger.error("Пользователь %s сделал неправильный выбор: %s" % (message.chat.id, text))
        user.SendMessage(text= M.ERROR_WRONG_CHOICE)

@bot.callback_query_handler(func = lambda call: call.data == B.CALL_SEARCH_GP and
                            User(call.message).GetUserState() > 2)
def change_s_gp(call):
    bot.answer_callback_query(call.id)
    user = User(call.message, bot)
    user.SendMessage(text='Давайте определим, чьё расписание мы ищем. Введите группу, Фамилию/ФИО преподавателя или кабинет.',
                    raw=False,
                    reply_markup=back_kb,
                    state=S.SEARCH_GP)

@bot.callback_query_handler(func = lambda call: call.data == B.CALL_SEARCH_DAY and
                            User(call.message).GetUserState() > 2)
def change_s_day(call):
    user = User(call.message, bot)
    user.SendMessage(text='Выберите день.',
                    raw=False,
                    reply_markup=day_choose_search_kb,
                    state=S.SEARCH_DAY)

@bot.callback_query_handler(func = lambda call: call.data == B.CALL_SEARCH_T)
def Send_search_t(call):
    user = User(call.message, bot)
    bot.answer_callback_query(call.id)
    user.EditMessageReplyMarkup()
    try:
        s = search.pop(user.id)
    except:
        s = None
    if(s != None):
        s[1] = s[1].lower()
        if(s[1] in day_to_number):
            res = GetTimetable(name = s[0], weekday= day_to_number[s[1]])
        elif(s[1] == B.TODAY.lower()):
            res = GetTimetable(name = s[0], day = 0)
        elif(s[1] == B.TOMORROW.lower()):
            res = GetTimetable(name = s[0], day = 1)
        user.SendMessage(text= res, raw=False)
        user.BackToMain()

