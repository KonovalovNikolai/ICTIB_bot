import logging
import re

from telebot import types

from DB_Helper.RedisHelper import set_state, get_current_state, get_message
from DB_Helper.SQLHelper import SQLHelper
from Serega.send_message import send_message
from Serega.ToTheMain import BackToMain
from Misc import message as M
from Misc import states as S
from Misc import buttons as B
from .markups import start_markup as m
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
    chat_id = message.chat.id

    db_worker = SQLHelper()

    if (db_worker.IsInBD(chat_id)):
        start_logger.error('Пользователь %s обновил UI' % chat_id)
        BackToMain(chat_id, "Интерфейс обновлён.") #ответ пользователю
    else:
        start_logger.error('Пользователь %s начал регистрацию' % chat_id)
        send_message(chat_id= chat_id, 
                    text = get_message(M.Start_Greetings) ,
                    reply_markup=m.start_markup_kb)
        set_state(chat_id, S.START)

    db_worker.close()

#Регистрация
@bot.message_handler(func = lambda message: get_current_state(message.chat.id) == S.START)
def user_entering_type(message):
    """
    Начало регистрации пользователя.
    Узнаём к каому типу относится пользователь.
    Если он абитуриент, то регистрация заганчивается.
    """
    chat_id = message.chat.id
    text = message.text.lower()
    
    if (text == B.Start_Stud.lower()):
        send_message(chat_id= chat_id, 
                    text= get_message(M.Start_Student) , 
                    reply_markup = types.ReplyKeyboardRemove())

        start_logger.error('Пользователь %s продолжил регистрацию как студент' % chat_id)
        
        set_state(chat_id, S.START_STUD)

    elif (text == B.Start_Teach.lower()):
        bot.send_message(chat_id= chat_id,
                        text= get_message(M.Start_Teacher) ,
                        reply_markup = types.ReplyKeyboardRemove())

        start_logger.error('Пользователь %s продолжил регистрацию как препод' % chat_id)
        
        set_state(chat_id, S.START_TEACH)

    elif (text == B.Start_Abitur.lower()):
        BackToMain(chat_id, get_message(M.Start_Abiturient))

        db_worker = SQLHelper()
        db_worker.AddUser(user = (chat_id, "abiturient", "abiturient",0))
        db_worker.close()

        start_logger.error('Пользователь %s зарегистрировался как абитуриент' % chat_id)

    else:
        send_message(chat_id, get_message(M.Error_Wrong_Choice))

        start_logger.error("Пользователь %s сделал неправильный выбор: %s" % (chat_id, text))

#Запись группы студента
@bot.message_handler(func = lambda message: get_current_state(message.chat.id) == S.START_STUD)
def user_entering_stud_group(message):
    """
    Спрашиваем студента о его группе
    """
    chat_id = message.chat.id
    text = message.text.lower()
    
    if (7 <= len(text) <= 8 and re.fullmatch(r'кт[абсм][зо][1-5]-[0-9]+', text)):
        text = text[0:2].upper() + text[2:4].lower() + text[4:] #Приводим группу к нужному формату
        
        start_logger.error('Пользователь %s ввёл свою группу: %s' % (chat_id, text))

        db_worker = SQLHelper()
        db_worker.AddUser(user = (chat_id, "stud", text, 0))
        db_worker.close()
        
        BackToMain(chat_id, get_message(M.Start_thanks))
    
    else:
        start_logger.error("Пользователь %s неправильно ввёл группу: %s" % (chat_id, text))
        
        send_message(chat_id = chat_id,
                        text= get_message(M.Error_Wrong_Input))

#Запись имени препада
@bot.message_handler(func = lambda message: get_current_state(message.chat.id) == S.START_TEACH)
def user_entering_tech_name(message):
    chat_id = message.chat.id #id чата
    text = message.text.lower() #введённое ФИО
    
    if (re.fullmatch(r'\w+ \w[.] \w[.]', text)):
        text = text[0].upper() + text[1:]#Приводим текст к нужному формату
        
        for i in re.finditer(r'\w[.]', text):
            text = text[:i.start()] + text[i.start()].upper() + text[i.start()+1:]

        start_logger.error('Пользователь %s ввёл инициалы: %s' % (chat_id, text))

        db_worker = SQLHelper()
        db_worker.AddUser(user = (chat_id, "teach", text,0))
        db_worker.close()
        
        BackToMain(chat_id, get_message(M.Start_thanks))
    
    else:
        start_logger.error("Пользователь %s некорректно ввёл инициалы: %s" % (chat_id, text))

        send_message(chat_id = chat_id,
                        text= get_message(M.Error_Wrong_Input) )