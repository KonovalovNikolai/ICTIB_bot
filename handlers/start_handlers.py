from config import bot
from Misc.states import States
from Misc.message import Message
from DB_Helper.SQLHelper import SQLHelper
from DB_Helper.RedisHelper import set_state, get_current_state, get_message
from telebot import types
from .markups import start_markup as m
from Serega.ToTheMain import BackToMain
import re
import logging

start_logger = logging.getLogger('Bot.start_handle')

#Обработка команды старт
#Если пользователя нет в бд, то начинаем регистрацию
#Если есть, то обновляем итерфейс и состояние
@bot.message_handler(commands = ['start'])
def command_handler(message):
    chat_id = message.chat.id

    db_worker = SQLHelper()

    if db_worker.IsInBD(chat_id):
        start_logger.error('User %s reloaded UI' % chat_id)
        BackToMain(chat_id, "Интерфейс обновлён.") #ответ пользователю
    else:
        start_logger.error('User %s started registration' % chat_id)
        bot.send_message(chat_id= chat_id, 
                        text = get_message(Message.M_Start_Greetings.value) ,
                        reply_markup=m.start_markup_kb)
        set_state(chat_id, States.S_START.value)

    db_worker.close()

#Регистрация
#Узнаём тип пользователя
@bot.message_handler(func = lambda message: get_current_state(message.chat.id) == States.S_START.value)
def user_entering_type(message):
    chat_id = message.chat.id
    text = message.text.lower()
    
    if text == "я студент!":
        start_logger.error('User %s continued registration as a student' % chat_id)
        
        set_state(chat_id, States.S_START_STUD.value)
        
        bot.send_message(chat_id= chat_id, 
                        text= get_message(Message.M_Start_Student.value) , 
                        reply_markup = types.ReplyKeyboardRemove())

    elif text == "я преподаватель!":
        start_logger.error('User %s continued registration as a teacher' % chat_id)
        
        set_state(chat_id, States.S_START_TEACH.value)
        
        bot.send_message(chat_id= chat_id,
                        text= get_message(Message.M_Start_Teacher.value) ,
                        reply_markup = types.ReplyKeyboardRemove())

    elif text == "я абитуриент!":
        start_logger.error('User %s was registered as an abiturient' % chat_id)
        
        db_worker = SQLHelper()
        db_worker.AddUser(user = (chat_id, "abiturient", "abiturient",0))
        db_worker.close()

        BackToMain(chat_id, get_message(Message.M_Start_Abiturient.value))
    else:
        start_logger.error("User %s made wrong choice: %s" % (chat_id, text))
        bot.send_message(chat_id, get_message(Message.M_Error_Wrong_Choice.value))

#Запись группы студента
@bot.message_handler(func = lambda message: get_current_state(message.chat.id) == States.S_START_STUD.value)
def user_entering_stud_group(message):
    chat_id = message.chat.id
    text = message.text.lower()
    
    if  7 <= len(text) <= 8 and re.fullmatch(r'кт[абсм][зо][1-5]-[0-9]+', text):
        text = text[0:2].upper() + text[2:4].lower() + text[4:] #Приводим группу к нужному формату
        
        start_logger.error('User %s entered his group: %s' % (chat_id, text))

        db_worker = SQLHelper()
        db_worker.AddUser(user = (chat_id, "stud", text, 0))
        
        BackToMain(chat_id, get_message(Message.M_Start_thanks.value))
        
        db_worker.close()
    
    else:
        start_logger.error("User %s made an invalid entry: %s" % (chat_id, text))
        
        bot.send_message(chat_id = chat_id,
                        text= get_message(Message.M_Error_Wrong_Input.value))

#Запись имени препада
@bot.message_handler(func = lambda message: get_current_state(message.chat.id) == States.S_START_TEACH.value)
def user_entering_tech_name(message):
    chat_id = message.chat.id #id чата
    text = message.text.lower() #введённое ФИО
    
    if re.fullmatch(r'\w+ \w[.] \w[.]', text):
        text = text[0].upper() + text[1:]#Приводим текст к нужному формату
        
        for i in re.finditer(r'\w[.]', text):
            text = text[:i.start()] + text[i.start()].upper() + text[i.start()+1:]

        start_logger.error('User %s entered his name: %s' % (chat_id, text))

        db_worker = SQLHelper()
        db_worker.AddUser(user = (chat_id, "teach", text,0))
        
        db_worker.close()
        
        BackToMain(chat_id, get_message(Message.M_Start_thanks.value))
    
    else:
        start_logger.error("User %s made an invalid entry: %s" % (chat_id, text))

        bot.send_message(chat_id = chat_id,
                        text= get_message(Message.M_Error_Wrong_Input.value) )