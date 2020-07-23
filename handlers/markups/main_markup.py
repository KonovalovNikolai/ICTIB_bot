from telebot import types


#Основная клавиатура
#Для студентов
main_markup_stud_kb = types.ReplyKeyboardMarkup(resize_keyboard= True)
#Для преподов
main_markup_teach_kb = types.ReplyKeyboardMarkup(resize_keyboard= True)
#Для абитуриентов
main_markup_abiturient_kb = types.ReplyKeyboardMarkup(resize_keyboard= True)
#Кнопки
btn_1 = types.KeyboardButton('Расписание')


main_markup_stud_kb.row(btn_1)

main_markup_teach_kb.row(btn_1)