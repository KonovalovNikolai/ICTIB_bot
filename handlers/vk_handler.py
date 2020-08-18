import logging

from telebot import types

from DB_Helper.SQLHelper import SQLHelper
from DB_Helper.RedisHelper import get_message, get_current_state, set_state
from Serega.Send_message import Send_message
from Serega.ToTheMain import BackToMain
from .Markups import buildings_kb
from Misc import B , S, M
from config import bot

def create_kb(vk):
    kb = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text = B.VK1 + '✔️' if vk[0] else B.VK1 + '❌', callback_data= 'vk1')
    btn2 = types.InlineKeyboardButton(text = B.VK2 + '✔️' if vk[1] else B.VK2 + '❌', callback_data= 'vk2')
    btn3 = types.InlineKeyboardButton(text = B.VK3 + '✔️' if vk[2] else B.VK3 + '❌', callback_data= 'vk3')
    kb.add(btn1, btn2, btn3)
    return kb

@bot.message_handler(func = lambda message: message.text == B.FOLLOWS
                    and get_current_state(message.chat.id) == S.NORMAL)
def send_inline_follow_menu(message):
    chat_id = message.chat.id

    db = SQLHelper()
    vk = db.TakeInfo(chat_id)[4:]
    db.close()

    Send_message(chat_id= chat_id,
                text='Придумайте, что должен отвечать бот. Ну серьёзно, я в тупике.\n❌: так отмеченны неотслеживаемые группы.\n✔️: а так - отслеживаемые',
                reply_markup=create_kb(vk),
                raw=False)

@bot.callback_query_handler(func = lambda call: call.data.startswith('vk'))
def set_inline_follow(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    vk = call.data[2]

    db = SQLHelper()
    db.UpdateVK(chat_id, vk)
    vk = db.TakeInfo(chat_id)[4:]
    db.close()

    bot.edit_message_reply_markup(chat_id=chat_id,
                                message_id=message_id,
                                reply_markup=create_kb(vk))
