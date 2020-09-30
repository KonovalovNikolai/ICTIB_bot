from Serega.User_Class import User
from config import bot

@bot.callback_query_handler(func = lambda call: True)
def End(call):
    # ответ на нажатие встроенных кнопок, которые не были обработаны
    bot.answer_callback_query(call.id)