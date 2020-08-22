import logging

from telebot import types

from DB_Helper.RedisHelper import get_message
from Serega.Send_message import Send_message
from .Markups import buildings_kb
from Misc import B
from config import bot

Buildings = {
    B.BUILD_G : ['Корпус «Г».', 47.2030488, 38.9346782, B.CALL_BUILD_G],
    B.BUILD_D : ['Корпус «Д».', 47.2022201, 38.9353249, B.CALL_BUILD_D],
    B.BUILD_I : ['Корпус «И».', 47.2039956, 38.9434289, B.CALL_BUILD_I],
    B.BUILD_A : ['Корпус «А».\nЦентр Довузовской Подготовки.',47.2052272,38.9396203, B.CALL_BUILD_A],
    B.BUILD_E : '',
    B.BUILD_K : '',
    B.BUILD_V : '',
    B.BUILD_B : ''
}

BuildsInfo = {
    B.CALL_BUILD_G : 'cock',
    B.CALL_BUILD_D : '',
    B.CALL_BUILD_I : '',
    B.CALL_BUILD_A : '',
    B.CALL_BUILD_E : '',
    B.CALL_BUILD_K : '',
    B.CALL_BUILD_V : '',
    B.CALL_BUILD_B : ''
}

buildings_kb.add(*[types.InlineKeyboardButton(text= i, callback_data= i) for i in Buildings.keys()])

@bot.message_handler(func = lambda message: message.text == B.BUILDINGS)
def send_buildings_list(message):
    Send_message(chat_id = message.chat.id,
                text = 'Выбирете корпус',
                reply_markup=buildings_kb,
                raw=False)

@bot.callback_query_handler(func = lambda call: call.data in Buildings)
def send_build_info(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    build = Buildings[call.data]

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton('Доп. информация', callback_data=build[3]))

    bot.edit_message_text(build[0], chat_id=chat_id, message_id= message_id)
    bot.send_location(chat_id= chat_id, latitude= build[1], longitude = build[2], reply_markup=kb)

@bot.callback_query_handler(func = lambda call: call.data in BuildsInfo)
def send_info(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    bot.edit_message_reply_markup(chat_id=chat_id, message_id= message_id)

    Send_message(chat_id= chat_id,
                text= BuildsInfo[call.data],
                raw=False)