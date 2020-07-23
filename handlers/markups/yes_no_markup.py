from telebot import types

yes_no_kb =types.ReplyKeyboardMarkup(resize_keyboard= True)
btn_yes = types.KeyboardButton("Да")
btn_no = types.KeyboardButton("Нет")
yes_no_kb.add(btn_yes, btn_no)