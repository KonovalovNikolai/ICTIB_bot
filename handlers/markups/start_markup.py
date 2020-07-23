from telebot import types

#/start
#Спрашиваем тип пользователя
start_markup_kb = types.ReplyKeyboardMarkup(resize_keyboard= True, row_width= 1)

btn_1 = types.KeyboardButton('Я студент!')
btn_2 = types.KeyboardButton('Я преподаватель!')
btn_3 = types.KeyboardButton('Я абитуриент!')

start_markup_kb.add(btn_1, btn_2, btn_3)