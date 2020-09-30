import logging
import re

from telebot import types

from Serega.User_Class import User
from Misc import *
from .Markups import start_markup_kb
from config import bot

logger = logging.getLogger('Bot.StartHandler')

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
        logger.error(f'User {user.id} reload UI.')
        user.BackToMain(M.UI_RELOAD) #ответ пользователю
    else:
        logger.error(f'User {user.id} started registration.')
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
        logger.error(f'User {user.id} continued registration as student.')

    elif (text == B.START_TEACH):
        user.SendMessage(text= M.START_TEACHER,
                        reply_markup = types.ReplyKeyboardRemove(),
                        state=S.START_TEACH)
        logger.error(f'User {user.id} continued registration as teacher.')

    elif (text == B.START_ABITUR):
        user.AddUser(U.ABITUR, U.ABITUR)
        user.BackToMain(M.START_ABITUR)
        logger.error(f'User {user.id} ended registration as abiturient.')

    else:
        user.SendMessage(text = M.ERROR_WRONG_CHOICE)
        logger.error(f"User {user.id} made wrong choice: {message.text}.")

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
        logger.error(f'User {user} ended registation as student: {text}')
    else:
        user.SendMessage(text= M.ERROR_WRONG_INPUT)
        logger.error(f'User {user.id} incorrectly entered a group: {text}')

#Запись имени препада
@bot.message_handler(func = lambda message: User(message).GetUserState() == S.START_TEACH)
def user_entering_tech_name(message):
    user = User(message, bot)
    text = message.text.lower() #введённое ФИО

    user.AddUser(U.TEACH, text)
    user.BackToMain(M.START_THANKS)

    logger.error(f'User {user} ended registation as teacher: {text}')