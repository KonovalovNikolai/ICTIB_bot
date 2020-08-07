import time

from config import bot

def Kludge():
    while True:
        time.sleep(60)
        try:
            bot.send_message(chat_id=1018144681,
                            text='Kludge')
        except:
            break