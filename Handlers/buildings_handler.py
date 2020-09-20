from requests import ConnectionError
import logging

from telebot import types

from Serega.User_Class import User
from .Markups import buildings_kb
from Misc import B, M
from config import bot

Buildings = {
    B.BUILD_G : [M.BUILDING_G, 47.2030488, 38.9346782, B.CALL_BUILD_G],
    B.BUILD_D : [M.BUILDING_D, 47.2022201, 38.9353249, B.CALL_BUILD_D],
    B.BUILD_I : [M.BUILDING_I, 47.2039956, 38.9434289, B.CALL_BUILD_I],
    B.BUILD_A : [M.BUILDING_A, 47.2052272, 38.9396203, B.CALL_BUILD_A],
    B.BUILD_E : [M.BUILDING_E, 47.2052272, 38.9396203, B.CALL_BUILD_A],
    B.BUILD_K : [M.BUILDING_K, 47.2052272, 38.9396203, B.CALL_BUILD_A],
    B.BUILD_V : [M.BUILDING_V, 47.2052272, 38.9396203, B.CALL_BUILD_A],
    B.BUILD_B : [M.BUILDING_B, 47.2052272, 38.9396203, B.CALL_BUILD_A]
}

BuildsInfo = {
    B.CALL_BUILD_G : M.BUILDING_INFO_G,
    B.CALL_BUILD_D : M.BUILDING_INFO_D,
    B.CALL_BUILD_I : M.BUILDING_INFO_I,
    B.CALL_BUILD_A : M.BUILDING_INFO_A,
    B.CALL_BUILD_E : M.BUILDING_INFO_E,
    B.CALL_BUILD_K : M.BUILDING_INFO_K,
    B.CALL_BUILD_V : M.BUILDING_INFO_V,
    B.CALL_BUILD_B : M.BUILDING_INFO_B
}

buildings_kb.add(*[types.InlineKeyboardButton(text= i, callback_data= i) for i in Buildings.keys()])

@bot.message_handler(func = lambda message: message.text == B.BUILDINGS)
def send_buildings_list(message):
    User(message, bot).SendMessage(text = M.CHOOSE_BUILD,
                                reply_markup=buildings_kb)

@bot.callback_query_handler(func = lambda call: call.data in Buildings)
def send_build_info(call):
    user = User(call.message, bot)

    bot.answer_callback_query(call.id)

    build = Buildings[call.data]
    buildings_info_kb = types.InlineKeyboardMarkup()
    buildings_info_kb.add(types.InlineKeyboardButton(B.BUILD_INFO, callback_data=build[3]))

    user.SendMessage(text=build[0])
    user.SendLocation(building=build, reply_markup=buildings_info_kb)

@bot.callback_query_handler(func = lambda call: call.data in BuildsInfo)
def send_info(call):
    user = User(call.message, bot)
    user.EditMessageReplyMarkup()
    user.SendMessage(text= BuildsInfo[call.data])