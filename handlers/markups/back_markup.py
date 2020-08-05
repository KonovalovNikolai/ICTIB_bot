from telebot import types

from Misc import buttons as B

back_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
back_kb.add(B.BACK)