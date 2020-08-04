from telebot import types
from Misc import buttons as B


#Основная клавиатура
#Для студентов
main_markup_stud_kb = types.ReplyKeyboardMarkup(resize_keyboard= True)
#Для преподов
main_markup_teach_kb = types.ReplyKeyboardMarkup(resize_keyboard= True)
#Для абитуриентов
main_markup_abiturient_kb = types.ReplyKeyboardMarkup(resize_keyboard= True)

main_markup_stud_kb.row(B.MAIN_MENU_TTABLE)

main_markup_teach_kb.row(B.MAIN_MENU_TTABLE)

main_markup_abiturient_kb.row(B.QUESTION)