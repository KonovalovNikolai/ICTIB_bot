import logging

from telebot import types

from Serega.User_Class import User
from .Markups import yes_no_kb, start_markup_kb
from Misc import *
from config import bot

logger = logging.getLogger("Bot.SettingsHandler")

def CreateSettingKb(user_type, user_group):
    kb = types.ReplyKeyboardMarkup()

    if (user_type == U.ABITUR):
        kb.add(B.TYPE + U.RU_ABITUR)
    else:
        if (user_type == U.STUDENT):
            kb.add(B.TYPE + U.RU_STUDENT)
            kb.add(B.GROUP + user_group)
        else:
            kb.add(B.TYPE + U.RU_TEACH)
            kb.add(B.NAME + user_group)

    kb.add(B.CONTACT, B.INFO)
    kb.add(B.DELETE)
    kb.add(B.BACK)

    return kb

@bot.message_handler(func = lambda message: message.text == B.SETTINGS
                        and User(message).GetUserState() == S.NORMAL)
def choose_settings(message):
    user = User(message, bot)
    user.GetUserInfo()

    user.SendMessage(text= M.SETTINGS_MENU,
                    reply_markup= CreateSettingKb(user.type, user.group),
                    state=S.SETTINGS)
    logger.error(f"User {user.id} got a settings menu.")

@bot.message_handler(func = lambda message: User(message).GetUserState() == S.SETTINGS)
def settings_menu(message):
    user = User(message, bot)

    text = message.text

    if (text == B.CONTACT):
        user.SendMessage(text= M.DEV)
        logger.error(f"User {user.id} got a developers contacts.")
    elif (text == B.INFO):
        user.SendMessage(text= M.ABOUT)
        logger.error(f"User {user.id} got a bot information.")
    elif (text == B.DELETE):
        user.SendMessage(text = M.CLEAR_СONFIRMATION,
                        reply_markup = yes_no_kb,
                        state=S.CLEAR)
        logger.error(f"User {user.id} got deletion confirmation button.")
    elif (text.startswith(B.TYPE)):
        user.DeleteUserSQL()
        user.SendMessage(text= M.CHANGE_TYPE,
                        reply_markup= start_markup_kb,
                        state=S.START)
        logger.error(f"User {user.id} changed user type.")
    elif (text.startswith(B.GROUP)):
        user.DeleteUserSQL()
        user.SendMessage(text= M.CHANGE_GROUPE,
                    reply_markup= types.ReplyKeyboardRemove(),
                    state=S.START_STUD)
        logger.error(f"User {user.id} changed user group.")
    elif (text.startswith(B.NAME)):
        user.DeleteUserSQL()
        user.SendMessage(text= M.CHANGE_NAME,
                        reply_markup= types.ReplyKeyboardRemove(),
                        state=S.START_TEACH)
        logger.error(f"User {user.id} changed user name.")
    else:
        user.SendMessage(text = M.ERROR_WRONG_CHOICE)
        logger.error(f"User {user.id} made wrong choice: {message.text}.")