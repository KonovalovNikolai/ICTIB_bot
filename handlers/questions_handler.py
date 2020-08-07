import logging
import pprint

from Misc import *
from DB_Helper.RedisHelper import set_state, get_current_state, get_message
from DB_Helper.SQLHelper import SQLHelper
from Serega.ToTheMain import BackToMain
from Serega.Send_message import Send_message
from .Markups import back_kb, del_quest_kb
from config import bot

quest_logger = logging.getLogger('Bot.question_handler')

@bot.message_handler(func = lambda message: message.text == B.QUESTION
                        and get_current_state(message.chat.id) == S.NORMAL)
def ask_question(message):
    chat_id = message.chat.id

    db = SQLHelper()
    user_type = db.TakeInfo(chat_id)[1]

    if (user_type == U.ABITUR):
        quest = db.TakeQuest(chat_id)
        if (quest):
            Send_message(chat_id= chat_id,
                        text= 'У вас уже есть заданный вопрос:\n<i>' + quest + '</i>',
                        reply_markup=del_quest_kb, parse_mode='HTML')
        else:
            bot.send_message(chat_id= chat_id,
                        text= '''
Всё, что вы хотели знать об институте, но боялись спросить.\n
Теперь абитуриенты могут задавать вопросы студентам, при этом сохраняя анонимность.
Просто напишите мне ваш вопрос, а я найду студента, который ответит на ваш вопрос.
Пожалуйста, соблюдайте правила приличия, задавая вопрос.
Также убедитесь, что ответа на ваш вопрос нет в разделе "Частые вопросы".''',
                        reply_markup= back_kb)
            set_state(chat_id, S.QUESTION)
    db.close()

@bot.message_handler(func = lambda message: get_current_state(message.chat.id) == S.QUESTION)
def writing_quest(message):
    chat_id = message.chat.id
    text = message.text

    db = SQLHelper()
    db.AddQuest(chat_id, message.message_id, text)
    db.close()

    bot.send_message(chat_id= chat_id,
                text= 'Я записал ваш вопрос. Скоро на него ответят.')
    BackToMain(chat_id)

@bot.callback_query_handler(func = lambda call: call.data == 'DeleteQuestion')
def DeleteQuestion(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    db = SQLHelper()
    db.DeleteQuest(chat_id)
    db.close()

    bot.edit_message_text(text= 'Вопрос удалён.',
                        chat_id= chat_id,
                        message_id= message_id)
