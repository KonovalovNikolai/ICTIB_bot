import logging
import re

from Misc import *
from DB_Helper.RedisHelper import set_state, get_current_state, get_message, brige_to_quest, get_quest_id
from DB_Helper.SQLHelper import SQLHelper
from Serega.ToTheMain import BackToMain
from Serega.Send_message import Send_message
from .Markups import back_kb, del_quest_kb, answer_kb
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
                        text= 'У вас уже есть заданный вопрос:\n<i>Вопрос №{}\n{}</i>'.format(quest[1], quest[2]),
                        reply_markup=del_quest_kb, parse_mode='HTML',
                        raw=False)
        else:
            Send_message(chat_id= chat_id,
                        text= '''
Всё, что вы хотели знать об институте, но боялись спросить.\n
Теперь абитуриенты могут задавать вопросы студентам, при этом сохраняя анонимность.
Просто напишите мне ваш вопрос, а я найду студента, который ответит на ваш вопрос.
Пожалуйста, соблюдайте правила приличия, задавая вопрос.
Также убедитесь, что ответа на ваш вопрос нет в разделе "Частые вопросы".''',
                        reply_markup= back_kb,
                        raw=False)
            set_state(chat_id, S.QUESTION)
    db.close()

@bot.message_handler(func = lambda message: get_current_state(message.chat.id) == S.QUESTION)
def writing_quest(message):
    chat_id = message.chat.id
    text = message.text

    db = SQLHelper()
    db.AddQuest(chat_id, message.message_id, text)
    db.close()

    Send_message(chat_id= chat_id,
                text= 'Я записал ваш вопрос. Скоро на него ответят.',
                raw=False)
    BackToMain(chat_id)

@bot.message_handler(func = lambda message: get_current_state(message.chat.id) == S.WRITE_ANSWER)
def Write_answer(message):
    chat_id = message.chat.id

    quest_id = get_quest_id(chat_id)

    Send_message(chat_id= chat_id,
                text= 'Ответ отправлен.',
                raw=False)
    BackToMain(chat_id)
    if(quest_id):
        db = SQLHelper()
        quest = db.TakeQuestWithId(quest_id)
        db.DeleteQuest(quest[0])
        db.close()

        Send_message(chat_id= quest[0],
                    text='На ваш вопрос ответили!\nВаш вопрос:\n<i>{}</i>'.format(quest[2]),
                    raw=False,
                    parse_mode='HTML')
        Send_message(chat_id= quest[0],
                    text='Ответ:\n<i>{}</i>'.format(message.text),
                    raw=False,
                    parse_mode='HTML')
        

@bot.message_handler(func = lambda message: message.text == B.ANSWER
                                and get_current_state(message.chat.id) == S.NORMAL)
def show_quest_for_stud(message):
    chat_id = message.chat.id

    db = SQLHelper()
    quest = db.TakeFirsQuest()
    db.close()

    if (quest):
        Send_message(chat_id= chat_id,
                    text='Вопрос №{}\n<i>{}</i>'.format(*quest),
                    reply_markup=answer_kb,
                    parse_mode='HTML',
                    raw=False)
    else:
        Send_message(chat_id= chat_id,
                    text='Вопросов пока нет.',
                    raw=False)

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

@bot.callback_query_handler(func = lambda call: call.data == 'AnswerQuestion'
                                and get_current_state(call.message.chat.id) >= S.NORMAL)
def WriteAnswer(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    bot.edit_message_reply_markup(chat_id=chat_id,
                                message_id= message_id)
    
    db = SQLHelper()
    user_type = db.TakeInfo(chat_id)[1]
    db.close()

    if(user_type == U.STUDENT):
        quest_id = call.message.text.split('\n')[0]
        quest_id = re.search(r'\d+', quest_id).group(0)
        
        brige_to_quest(chat_id, quest_id)

        Send_message(chat_id= chat_id,
                    text='Введите ваш ответ.',
                    reply_markup=back_kb,
                    raw=False)
        set_state(chat_id, S.WRITE_ANSWER)

@bot.callback_query_handler(func = lambda call: call.data == 'NextQuestion'
                                and get_current_state(call.message.chat.id) >= S.NORMAL)
def NextQuest(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    db = SQLHelper()
    quest = db.TakeRandomQuest()
    db.close()

    bot.edit_message_text(chat_id= chat_id,
                        message_id= message_id,
                        text='Вопрос №{}\n<i>{}</i>'.format(*quest),
                        parse_mode='HTML')
    bot.edit_message_reply_markup(chat_id=chat_id,
                                message_id= message_id,
                                reply_markup=answer_kb)