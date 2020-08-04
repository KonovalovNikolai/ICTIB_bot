from config import bot
from DB_Helper.RedisHelper import get_message
import time

def send_message(chat_id, text, reply_markup=None):
    """
    Отправка сообщения с отловом ошибки 104,
    которая возникает, когда бот бездействует 10 минут,
    а потом получает сообщение от пользователя.
    """
    try:
        #Пробуем отправить сообщение
        bot.send_message(chat_id = chat_id,
                        text = text,
                        reply_markup = reply_markup)
    except:
        #Если поймали ошибку, то ждём 5 секунд и пробуем ещё раз
        time.sleep(3)
        send_message(chat_id = chat_id, text = text, reply_markup= reply_markup)
        
