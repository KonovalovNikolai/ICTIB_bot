import logging

from DB_Helper.RedisHelper import get_current_state
from Serega.ToTheMain import BackToMain
from Misc import states as S
from Misc import buttons as B
from config import bot

@bot.message_handler(func = lambda message: message.text == B.BACK
            and get_current_state(message.chat.id) not in 
                        (S.NORMAL, S.START, S.START_STUD, S.START_TEACH))
def go_back(message):
    chat_id = message.chat.id

    BackToMain(chat_id)