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
                        text = M.U_HAVE_QUEST,
                        form = quest[1:],
                        reply_markup = del_quest_kb,
                        parse_mode = 'HTML')
        else:
            Send_message(chat_id= chat_id,
                        text= M.ASK_QUESTION,
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

    BackToMain(chat_id, M.QUEST_WRITED)

@bot.message_handler(func = lambda message: message.text == B.ANSWER
                                and get_current_state(message.chat.id) == S.NORMAL)
def show_quest_for_stud(message):
    chat_id = message.chat.id

    db = SQLHelper()
    quest = db.TakeFirsQuest()
    db.close()

    if (quest):
        Send_message(chat_id= chat_id,
                    text=M.QUEST_FOR_YOU,
                    form = quest,
                    reply_markup=answer_kb,
                    parse_mode='HTML')
    else:
        Send_message(chat_id= chat_id,
                    text=M.NO_QUESTION)

@bot.message_handler(func = lambda message: get_current_state(message.chat.id) == S.WRITE_ANSWER)
def Write_answer(message):
    chat_id = message.chat.id

    quest_id = get_quest_id(chat_id)

    BackToMain(chat_id, M.ANSWER_SENDED)
    if(quest_id):
        db = SQLHelper()
        quest = db.TakeQuestWithId(quest_id)
        if quest:
            db.DeleteQuest(quest[0])
        db.close()

        if quest:
            Send_message(chat_id= quest[0],
                        text=M.ANSWER_FOR_YOU)

            Send_message(chat_id= quest[0],
                        text=message.text,
                        reply_to_message_id=quest_id,
                        raw=False)

@bot.callback_query_handler(func = lambda call: call.data == B.CALL_DELETE_QUEST)
def DeleteQuestion(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    db = SQLHelper()
    db.DeleteQuest(chat_id)
    db.close()

    bot.edit_message_text(text= 'Вопрос удалён.',
                        chat_id= chat_id,
                        message_id= message_id)

@bot.callback_query_handler(func = lambda call: call.data == B.CALL_SEND_ANSWER)
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
                    text=M.ENTER_ANSWER,
                    reply_markup=back_kb)
        set_state(chat_id, S.WRITE_ANSWER)

@bot.callback_query_handler(func = lambda call: call.data == B.CALL_NEXT)
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