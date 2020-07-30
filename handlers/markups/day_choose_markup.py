from telebot import types

from Misc import buttons as B

day_choose_kb = types.ReplyKeyboardMarkup(resize_keyboard= True, row_width=3)

day_choose_kb.add(B.Days_Mon, B.Days_Tue, B.Days_Wed)
day_choose_kb.add(B.Days_Thu, B.Days_Fri, B.Days_Sat)
day_choose_kb.row(B.Auto_Table)
day_choose_kb.row(B.Back)