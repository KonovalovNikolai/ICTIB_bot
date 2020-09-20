import logging
import re

from Serega.User_Class import User
from Misc import *
from .Markups import back_kb, del_quest_kb, answer_kb
from config import bot

quest_logger = logging.getLogger('Bot.question_handler')

@bot.message_handler(func = lambda message: message.text == B.QUESTION
                        and User(message).GetUserState() == S.NORMAL)
def ask_question(message):
    user = User(message, bot)
    user.GetUserInfo()
    if (user.type == U.ABITUR):
        quest = user.GetUserQuest()
        if (quest):
            user.SendMessage(text = M.U_HAVE_QUEST,
                            form = quest[1:],
                            reply_markup = del_quest_kb,
                            parse_mode = 'HTML')
        else:
            user.SendMessage(text= M.ASK_QUESTION,
                            reply_markup= back_kb,
                            state=S.QUESTION)

@bot.message_handler(func = lambda message: User(message).GetUserState() == S.QUESTION)
def writing_quest(message):
    user = User(message, bot)
    user.AddQuest(message.message_id, message.text)
    user.BackToMain(M.QUEST_WRITED)

@bot.message_handler(func = lambda message: message.text == B.ANSWER
                                and User(message).GetUserState() == S.NORMAL)
def show_quest_for_stud(message):
    user = User(message, bot)
    user.GetUserInfo()

    if(user.type == U.STUDENT):
        quest = user.GetFirstQuest()
        if (quest):
            user.SendMessage(text=M.QUEST_FOR_YOU,
                            form = quest,
                            reply_markup=answer_kb,
                            parse_mode='HTML')
        else:
            user.SendMessage(text=M.NO_QUESTION)

@bot.message_handler(func = lambda message: User(message).GetUserState() == S.WRITE_ANSWER)
def Write_answer(message):
    user = User(message, bot)

    quest_id = user.GetQuestBrige()

    user.BackToMain(M.ANSWER_SENDED)

    if(quest_id):
        quest = user.GetQuestById(message.id)

        if quest:
            user.SendMessageToAnotherUser(chat_id= quest[0],
                                        text=M.ANSWER_FOR_YOU)
            try:
                user.SendMessageToAnotherUser(chat_id= quest[0],
                                            text=message.text,
                                            reply_to_message_id=quest_id,
                                            raw=False)
            except:
                user.SendMessageToAnotherUser(chat_id= quest[0],
                                            text='<i>{}</i>\n{}'.format(quest[2], message.text),
                                            parse_mode='HTML',
                                            raw=False)

@bot.callback_query_handler(func = lambda call: call.data == B.CALL_DELETE_QUEST)
def DeleteQuestion(call):
    user = User(call.message, bot)
    user.DeleteQuest()
    user.EditMessageText(text=M.QUEST_DELETED)

@bot.callback_query_handler(func = lambda call: call.data == B.CALL_SEND_ANSWER)
def WriteAnswer(call):
    user = User(call.message, bot)
    user.EditMessageReplyMarkup()
    user.GetUserInfo()

    if(user.type == U.STUDENT):
        quest_id = call.message.text.split('\n')[0]
        quest_id = re.search(r'\d+', quest_id).group(0)
        
        user.SetQuestBrige(quest_id)
        user.SendMessage(text=M.ENTER_ANSWER,
                        reply_markup=back_kb,
                        state=S.WRITE_ANSWER)

@bot.callback_query_handler(func = lambda call: call.data == B.CALL_NEXT)
def NextQuest(call):
    user = User(call.message, bot)

    quest = user.GetRandomQuest()

    user.EditMessageText(text =M.QUEST_NUMBER,
                        form = quest,
                        parse_mode='HTML')
    user.EditMessageReplyMarkup(reply_markup=answer_kb)