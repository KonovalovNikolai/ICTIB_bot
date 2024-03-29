import logging

from telebot import types

from Serega.User_Class import User
from Serega.Timetable import GetTodayDate, GetTimetable
from Misc import *
from .Markups import day_choose_kb, back_kb, day_choose_search_kb
from config import bot

logger = logging.getLogger('Bot.TTHandler')

#Словарь для перевода дней недели в числа
day_to_number = {
    'понедельник':0,
    'вторник':1,
    'среда':2,
    'четверг':3,
    'пятница':4,
    'суббота':5
}

def CreateExpendKb(exp):
    expend_kb = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton(text = exp[0], callback_data= B.CALL_SEARCH_GP)
    btn2 = types.InlineKeyboardButton(text = exp[1], callback_data= B.CALL_SEARCH_DAY)
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
        logger.error(f'User {user.id} got a timetable menu.')

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
        user.BackToMain(text = res, raw= False)
        logger.error(f'User {user.id} got a timetable: {user.group}, {text}.')

    elif (text == B.TODAY.lower()):
        user.GetUserInfo()
        #Получаем расписание
        res = GetTimetable(name = user.group, day = 0)
        #Вывод расписания
        user.BackToMain(text = res, raw= False)
        logger.error(f'User {user.id} got a timetable: {user.group}, {text}.')

    elif (text == B.TOMORROW.lower()):
        user.GetUserInfo()
        #Получаем расписание
        res = GetTimetable(name = user.group, day = 1)
        #Вывод расписания
        user.BackToMain(text = res, raw= False)
        logger.error(f'User {user.id} got a timetable: {user.group}, {text}.')

    elif (text == B.EXTENDED_T.lower()):
        user.SetExpend()
        exp = user.GetExpend()
        user.SendMessage(text=M.EXPENDED_SEARCH,
                        form = exp,
                        reply_markup=CreateExpendKb(exp))
        logger.error(f'User {user.id} got a extended timetable menu.')

    #Авторасписание
    elif (text == B.AUTO_TABLE.lower()):
        #Меняем параметр авторасписания в бд
        ret = user.UpdateAuto()
        if ret:
            answer = M.AUTO_ON
        else:
            answer = M.AUTO_OFF
        user.BackToMain(answer)
        logger.error(f'User {user.id} changed auto tt: {ret}.')

    #Ничего из предложенного
    else:
        logger.error(f"User {user.id} made wrong choice: {message.text}.")
        user.SendMessage(text= M.ERROR_WRONG_CHOICE)

@bot.message_handler(func = lambda message: User(message).GetUserState() == S.SEARCH_GP)
def Set_GP(message):
    user = User(message, bot)
    user.SetExpend(group=message.text)
    exp = user.GetExpend()
    user.SendMessage(text=M.EXPENDED_SEARCH,
                        form = exp,
                        reply_markup=CreateExpendKb(exp))
    logger.error(f'User {user.id} entered group: {message.text}.')

@bot.message_handler(func = lambda message: User(message).GetUserState() == S.SEARCH_DAY)
def Set_Day(message):
    user = User(message, bot)
    text = message.text.lower()
    if(text in day_to_number or text == B.TODAY.lower() or text == B.TOMORROW.lower()):
        user.SetExpend(day=message.text)
        exp = user.GetExpend()
        user.SendMessage(text=M.EXPENDED_SEARCH,
                        form = exp,
                        reply_markup=CreateExpendKb(exp))
        logger.error(f'User {user.id} entered day: {message.text}.')
    else:
        logger.error(f"User {user.id} made wrong choice: {message.text}.")
        user.SendMessage(text= M.ERROR_WRONG_CHOICE)

@bot.callback_query_handler(func = lambda call: call.data == B.CALL_SEARCH_GP and
                            User(call.message).GetUserState() > 2)
def change_s_gp(call):
    bot.answer_callback_query(call.id)
    user = User(call.message, bot)
    user.SendMessage(text=M.EXPENDED_GP,
                    reply_markup=back_kb,
                    state=S.SEARCH_GP)
    logger.error(f'User {user.id} is entering group.')

@bot.callback_query_handler(func = lambda call: call.data == B.CALL_SEARCH_DAY and
                            User(call.message).GetUserState() > 2)
def change_s_day(call):
    user = User(call.message, bot)
    user.SendMessage(text=M.EXPENDED_DAY,
                    reply_markup=day_choose_search_kb,
                    state=S.SEARCH_DAY)
    logger.error(f'User {user.id} is entering day.')

@bot.callback_query_handler(func = lambda call: call.data == B.CALL_SEARCH_T)
def Send_search_t(call):
    user = User(call.message, bot)
    bot.answer_callback_query(call.id)
    #user.EditMessageReplyMarkup()
    exp = user.GetExpend()
    exp[1] = exp[1].lower()
    if(exp[1] in day_to_number):
        res = GetTimetable(name = exp[0], weekday= day_to_number[exp[1]])
    elif(exp[1] == B.TODAY.lower()):
        res = GetTimetable(name = exp[0], day = 0)
    elif(exp[1] == B.TOMORROW.lower()):
        res = GetTimetable(name = exp[0], day = 1)
    user.BackToMain(text= res, raw=False)
    logger.error(f'User {user.id} got a extended timetable: {exp[0]}, {exp[1]}.')

