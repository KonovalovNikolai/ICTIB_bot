from telebot import types

day_choose_kb = types.ReplyKeyboardMarkup(resize_keyboard= True, row_width=3)

btn_1 = types.KeyboardButton('Понедельник')
btn_2 = types.KeyboardButton('Вторник')
btn_3 = types.KeyboardButton('Среда')
btn_4 = types.KeyboardButton('Четверг')
btn_5 = types.KeyboardButton('Пятница')
btn_6 = types.KeyboardButton('Суббота')
btn_auto_tb = types.KeyboardButton('Авторасписание')
btn_back = types.KeyboardButton('Назад')

day_choose_kb.add(btn_1, btn_2, btn_3)
day_choose_kb.add(btn_4, btn_5, btn_6)
day_choose_kb.row(btn_auto_tb)
day_choose_kb.row(btn_back)