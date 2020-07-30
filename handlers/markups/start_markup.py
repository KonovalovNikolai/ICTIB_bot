from telebot import types
from Misc import buttons as B

#/start
#Спрашиваем тип пользователя
start_markup_kb = types.ReplyKeyboardMarkup(resize_keyboard= True, row_width= 1)

start_markup_kb.add(B.START_STUD, B.START_TEACH, B.START_ABITUR)