from telebot import types

from Misc import B

back_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
back_kb.add(B.BACK)

day_choose_kb = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
day_choose_kb.add(B.TODAY, B.TOMORROW)
day_choose_kb.add(B.DAYS_MON, B.DAYS_TUE, B.DAYS_WED)
day_choose_kb.add(B.DAYS_THU, B.DAYS_FRI, B.DAYS_SAT)
day_choose_kb.add(B.EXTENDED_T)
day_choose_kb.row(B.AUTO_TABLE)
day_choose_kb.row(B.BACK)

day_choose_search_kb = types.ReplyKeyboardMarkup(row_width=3)
day_choose_search_kb.add(B.TODAY, B.TOMORROW)
day_choose_search_kb.add(B.DAYS_MON, B.DAYS_TUE, B.DAYS_WED)
day_choose_search_kb.add(B.DAYS_THU, B.DAYS_FRI, B.DAYS_SAT)
day_choose_search_kb.row(B.BACK)

#Основная клавиатура
#Для студентов
main_markup_stud_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_markup_stud_kb.row(B.MAIN_MENU_TTABLE)
main_markup_stud_kb.add(B.ANSWER, B.FOLLOWS)
main_markup_stud_kb.add(B.BUILDINGS, 'Переcдачи', 'Персонал')
main_markup_stud_kb.row(B.SETTINGS)
#Для преподов
main_markup_teach_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_markup_teach_kb.row(B.MAIN_MENU_TTABLE)
main_markup_teach_kb.row(B.FOLLOWS)
main_markup_teach_kb.row(B.SETTINGS)
#Для абитуриентов
main_markup_abiturient_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_markup_abiturient_kb.row(B.QUESTION)
main_markup_abiturient_kb.row(B.FOLLOWS)
main_markup_abiturient_kb.row(B.BUILDINGS, 'Направления', 'Двери')
main_markup_abiturient_kb.row(B.SETTINGS)

#/start
#Спрашиваем тип пользователя
start_markup_kb = types.ReplyKeyboardMarkup(row_width= 1, resize_keyboard=True)
start_markup_kb.add(B.START_STUD, B.START_TEACH, B.START_ABITUR)

yes_no_kb =types.ReplyKeyboardMarkup(resize_keyboard=True)
yes_no_kb.add(B.YES, B.NO)

del_quest_kb = types.InlineKeyboardMarkup()
del_quest = types.InlineKeyboardButton(text = B.DELETE_QUEST, callback_data= B.CALL_DELETE_QUEST)
del_quest_kb.add(del_quest)

answer_kb = types.InlineKeyboardMarkup()
answer_btn = types.InlineKeyboardButton(text = B.SEND_ANSWER, callback_data= B.CALL_SEND_ANSWER)
next_quest_btn = types.InlineKeyboardButton(text = B.NEXT, callback_data= B.CALL_NEXT)
answer_kb.add(answer_btn, next_quest_btn)

buildings_kb = types.InlineKeyboardMarkup(row_width = 4)