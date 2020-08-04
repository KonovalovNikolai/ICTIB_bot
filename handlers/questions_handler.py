import logging

from DB_Helper.RedisHelper import set_state, get_current_state, get_message
from DB_Helper.SQLHelper import SQLHelper
from Serega.send_message import send_message
from Serega.ToTheMain import BackToMain
from Misc import message as M
from Misc import states as S
from Misc import buttons as B
from Misc import users as U
from config import bot

quest_logger = logging.getLogger('Bot.question_handler')

@bot.message_handler(func = lambda message: message.text.lower() == B.QUESTION.lower()
                        and get_current_state(message.chat.id) == S.NORMAL)
def ask_question(message):
    chat_id = message.chat.id

    db = SQLHelper()
    user_type = db.TakeInfo(chat_id)[1]
    db.close()

    if (user_type == U.ABITUR):
        send_message(chat_id= chat_id,
                    text= '''Всё, что вы хотели знать об институте, но боялись спросить.\n
                        Теперь абитуриенты могут задавать вопросы студентам, при этом сохраняя анонимность.
                        Просто напишите мне ваш вопрос, а я найду студента, который ответит на ваш вопрос.
                        Пожалуйста, соблюдайте правила приличия, задавая вопрос.
                        Также убедитесь, что ответа на ваш вопрос нет в разделе "Частые вопросы".''',
                    reply_markup= None) 