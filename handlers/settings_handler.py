import logging

from telebot import types

from DB_Helper.RedisHelper import set_state, get_current_state, get_message
from DB_Helper.SQLHelper import SQLHelper
from Serega.Send_message import Send_message
from Serega.ToTheMain import BackToMain
from .Markups import yes_no_kb, start_markup_kb
from Misc import *
from config import bot

def create_setting_kb(user_info = []):
    kb = types.ReplyKeyboardMarkup()

    if (user_info[1] == U.ABITUR):
        kb.add(B.TYPE + U.RU_ABITUR)
    else:
        if (user_info[1] == U.STUDENT):
            kb.add(B.TYPE + U.RU_STUDENT)
            kb.add(B.GROUP + user_info[2])
        else:
            kb.add(B.TYPE + U.RU_TEACH)
            kb.add(B.NAME + user_info[2])
        
        kb.add(B.ALERTS)
    
    kb.add(B.CONTACT, B.INFO)
    kb.add(B.DELETE)
    kb.add(B.BACK)

    return kb

@bot.message_handler(func = lambda message: get_current_state(message.chat.id) == S.NORMAL
                        and message.text == B.SETTINGS)
def choose_settings(message):
    chat_id = message.chat.id

    db = SQLHelper()
    user_info = db.TakeInfo(chat_id)
    db.close()

    kb = create_setting_kb(user_info)

    Send_message(chat_id= chat_id,
                text= M.SETTINGS_MENU,
                reply_markup= kb)
    set_state(chat_id, S.SETTINGS)

@bot.message_handler(func = lambda message: get_current_state(message.chat.id) == S.SETTINGS)
def settings_menu(message):
    chat_id = message.chat.id
    text = message.text

    if (text == B.CONTACT):
        Send_message(chat_id= chat_id,
                    text= M.DEV)
    elif (text == B.INFO):
        Send_message(chat_id= chat_id,
                    text= M.ABOUT)
    elif (text == B.ALERTS):
        pass
    elif (text == B.DELETE):
        Send_message(chat_id = chat_id,
                    text = M.CLEAR_СONFIRMATION,
                    reply_markup = yes_no_kb)

        set_state(chat_id, S.CLEAR)
    elif (text.startswith(B.TYPE)):
        db = SQLHelper()
        db.DeleteUser(chat_id)
        db.close()
        Send_message(chat_id= chat_id,
                    text= M.CHANGE_TYPE,
                    reply_markup= start_markup_kb)
        set_state(chat_id, S.START)
    elif (text.startswith(B.GROUP)):
        db = SQLHelper()
        db.DeleteUser(chat_id)
        db.close()

        Send_message(chat_id= chat_id,
                    text= M.CHANGE_GROUPE,
                    reply_markup= types.ReplyKeyboardRemove())
        set_state(chat_id, S.START_STUD)
    elif (text.startswith(B.NAME)):
        db = SQLHelper()
        db.DeleteUser(chat_id)
        db.close()

        Send_message(chat_id= chat_id,
                    text= M.CHANGE_NAME,
                    reply_markup= types.ReplyKeyboardRemove())
        set_state(chat_id, S.START_TEACH)
    else:
        Send_message(chat_id = chat_id,
                    text = M.ERROR_WRONG_CHOICE)