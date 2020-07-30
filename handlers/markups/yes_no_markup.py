from telebot import types
from Misc import buttons as B

yes_no_kb =types.ReplyKeyboardMarkup(resize_keyboard= True)

yes_no_kb.add(B.YES, B.NO)