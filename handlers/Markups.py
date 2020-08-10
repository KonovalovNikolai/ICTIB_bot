from telebot import types

from Misc import B

back_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
back_kb.add(B.BACK)

day_choose_kb = types.ReplyKeyboardMarkup(resize_keyboard= True, row_width=3)
day_choose_kb.add(B.DAYS_MON, B.DAYS_TUE, B.DAYS_WED)
day_choose_kb.add(B.DAYS_THU, B.DAYS_FRI, B.DAYS_SAT)
day_choose_kb.row(B.AUTO_TABLE)
day_choose_kb.row(B.BACK)

#Основная клавиатура
#Для студентов
main_markup_stud_kb = types.ReplyKeyboardMarkup(resize_keyboard= True)
main_markup_stud_kb.row(B.MAIN_MENU_TTABLE)
main_markup_stud_kb.row(B.ANSWER)
main_markup_stud_kb.row(B.SETTINGS)
#Для преподов
main_markup_teach_kb = types.ReplyKeyboardMarkup(resize_keyboard= True)
main_markup_teach_kb.row(B.MAIN_MENU_TTABLE)
main_markup_teach_kb.row(B.SETTINGS)
#Для абитуриентов
main_markup_abiturient_kb = types.ReplyKeyboardMarkup(resize_keyboard= True)
main_markup_abiturient_kb.row(B.QUESTION)
main_markup_abiturient_kb.row(B.SETTINGS)

#/start
#Спрашиваем тип пользователя
start_markup_kb = types.ReplyKeyboardMarkup(resize_keyboard= True, row_width= 1)
start_markup_kb.add(B.START_STUD, B.START_TEACH, B.START_ABITUR)

yes_no_kb =types.ReplyKeyboardMarkup(resize_keyboard= True)
yes_no_kb.add(B.YES, B.NO)

del_quest_kb = types.InlineKeyboardMarkup()
del_quest = types.InlineKeyboardButton(text = 'Удалить вопрос', callback_data= 'DeleteQuestion')
del_quest_kb.add(del_quest)

answer_kb = types.InlineKeyboardMarkup()
answer_btn = types.InlineKeyboardButton(text = 'Ответить', callback_data= 'AnswerQuestion')
next_quest_btn = types.InlineKeyboardButton(text = '>>>', callback_data= 'NextQuestion')
answer_kb.add(answer_btn, next_quest_btn)