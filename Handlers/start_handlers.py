import logging
import re

from telebot import types

from Serega.User_Class import User
from Misc import *
from .Markups import start_markup_kb
from config import bot

start_logger = logging.getLogger('Bot.start_handle')

#Обработка команды start
@bot.message_handler(commands = ['start'])
def command_handler(message):
    """
    Доступно с любого состояния
    Если пользователя нет в бд, то начинаем регистрацию
    Если есть, то обновляем итерфейс и состояние
    """
    user = User(message, bot)
    user.GetUserInfo()

    if (user.type != None):
        start_logger.error('Пользователь %s обновил UI' % message.chat.id)
        user.BackToMain(M.UI_RELOAD) #ответ пользователю
    else:
        start_logger.error('Пользователь %s начал регистрацию' % message.chat.id)
        user.SendMessage(text = M.START_GREETINGS,
                        reply_markup = start_markup_kb,
                        state = S.START)

#Регистрация
@bot.message_handler(func = lambda message: User(message).GetUserState() == S.START)
def user_entering_type(message):
    """
    Начало регистрации пользователя.
    Узнаём к каому типу относится пользователь.
    Если он абитуриент, то регистрация заганчивается.
    """
    user = User(message, bot)
    text = message.text

    if (text == B.START_STUD):
        user.SendMessage(text= M.START_STUDENT,
                        reply_markup = types.ReplyKeyboardRemove(),
                        state=S.START_STUD)
        start_logger.error('Пользователь %s продолжил регистрацию как студент' % message.chat.id)

    elif (text == B.START_TEACH):
        user.SendMessage(text= M.START_TEACHER,
                        reply_markup = types.ReplyKeyboardRemove(),
                        state=S.START_TEACH)
        start_logger.error('Пользователь %s продолжил регистрацию как препод' % message.chat.id)

    elif (text == B.START_ABITUR):
        user.AddUser(U.ABITUR, U.ABITUR)
        user.BackToMain(M.START_ABITUR)
        start_logger.error('Пользователь %s зарегистрировался как абитуриент' % message.chat.id)

    else:
        user.SendMessage(text = M.ERROR_WRONG_CHOICE)
        start_logger.error("Пользователь %s сделал неправильный выбор: %s" % (message.chat.id, text))

#Запись группы студента
@bot.message_handler(func = lambda message: User(message).GetUserState() == S.START_STUD)
def user_entering_stud_group(message):
    """
    Спрашиваем студента о его группе
    """
    user = User(message, bot)
    text = message.text.lower()

    if (7 <= len(text) <= 8 and re.fullmatch(r'кт[абсм][зо][1-5]-[0-9]+', text)):
        text = text[0:2].upper() + text[2:4].lower() + text[4:] #Приводим группу к нужному формату

        user.AddUser(U.STUDENT, text)
        user.BackToMain(M.START_THANKS)
        start_logger.error('Пользователь %s ввёл свою группу: %s' % (message.chat.id, text))
    else:
        user.SendMessage(text= M.ERROR_WRONG_INPUT)
        start_logger.error("Пользователь %s неправильно ввёл группу: %s" % (message.chat.id, text))

#Запись имени препада
@bot.message_handler(func = lambda message: User(message).GetUserState() == S.START_TEACH)
def user_entering_tech_name(message):
    user = User(message, bot)
    text = message.text.lower() #введённое ФИО

    if (re.fullmatch(r'\w+', text) or re.fullmatch(r'\w+ \w[.] \w[.]', text)):
        text = text[0].upper() + text[1:]#Приводим текст к нужному формату
        for i in re.finditer(r'\w[.]', text):
            text = text[:i.start()] + text[i.start()].upper() + text[i.start()+1:]

        user.AddUser(U.TEACH, text)
        user.BackToMain(M.START_THANKS)

        start_logger.error('Пользователь %s ввёл инициалы: %s' % (message.chat.id, text))
    else:
        start_logger.error("Пользователь %s некорректно ввёл инициалы: %s" % (message.chat.id, text))
        user.SendMessage(text = M.ERROR_WRONG_INPUT)