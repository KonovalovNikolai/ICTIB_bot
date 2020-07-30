from telebot import types
from Misc import buttons as B

#/start
#Спрашиваем тип пользователя
start_markup_kb = types.ReplyKeyboardMarkup(resize_keyboard= True, row_width= 1)

start_markup_kb.add(B.Start_Stud, B.Start_Teach, B.Start_Abitur)