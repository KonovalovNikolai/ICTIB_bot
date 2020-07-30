from telebot import types

from Misc import buttons as B

day_choose_kb = types.ReplyKeyboardMarkup(resize_keyboard= True, row_width=3)

day_choose_kb.add(B.DAYS_MON, B.DAYS_TUE, B.DAYS_WED)
day_choose_kb.add(B.DAYS_THU, B.DAYS_FRI, B.DAYS_SAT)
day_choose_kb.row(B.AUTO_TABLE)
day_choose_kb.row(B.BACK)