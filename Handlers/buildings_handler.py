import logging

from requests import ConnectionError
import logging

from telebot import types

from Serega.User_Class import User
from .Markups import buildings_kb
from Misc import B, M, S
from config import bot

logger = logging.getLogger("Bot.BuildingsHandler")

Buildings = {
    B.BUILD_G : [M.BUILDING_G, 47.2030488, 38.9346782, B.CALL_BUILD_G],
    B.BUILD_D : [M.BUILDING_D, 47.2021358, 38.9351968, B.CALL_BUILD_D],
    B.BUILD_I : [M.BUILDING_I, 47.2040998, 38.9435581, B.CALL_BUILD_I],
    B.BUILD_A : [M.BUILDING_A, 47.2052909, 38.939704, B.CALL_BUILD_A],
    B.BUILD_E : [M.BUILDING_E, 47.2044747, 38.9444894, B.CALL_BUILD_E],
    B.BUILD_K : [M.BUILDING_K, 47.2044747, 38.9444894, B.CALL_BUILD_K],
    B.BUILD_V : [M.BUILDING_V, 47.2165148, 38.9271022, B.CALL_BUILD_A],
    B.BUILD_B : [M.BUILDING_B, 47.2053781, 38.9388453, B.CALL_BUILD_A]
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

# генерация клавиатуры-списка зданий
buildings_kb.add(*[types.InlineKeyboardButton(text= i, callback_data= i) for i in Buildings.keys()])

@bot.message_handler(func = lambda message: message.text == B.BUILDINGS and
                        User(message).GetUserState == S.NORMAL)
def send_buildings_list(message):
    '''Отправка клавиатуры зданий'''
    user = User(message, bot)

    logger.error(f"User {user.id} got the buildings list.")

    # тправка клавиатуры
    user.SendMessage(
        text = M.CHOOSE_BUILD, reply_markup=buildings_kb
        )

@bot.callback_query_handler(func = lambda call: call.data in Buildings)
def send_building_locale(call):
    '''Обработка нажатий клавиш названий зданий'''
    user = User(call.message, bot)

    logger.error(f"User {user.id} chose building {call.data}.")

    # убрать статус ожидания ответа с нажатой кнопки
    bot.answer_callback_query(call.id)
    # кнопка доп. информации
    build = Buildings[call.data]
    buildings_info_kb = types.InlineKeyboardMarkup()
    buildings_info_kb.add(types.InlineKeyboardButton(B.BUILD_INFO, callback_data=build[3]))
    # отправка локации
    user.SendMessage(text=build[0])
    user.SendLocation(building=build, reply_markup=buildings_info_kb)

@bot.callback_query_handler(func = lambda call: call.data in BuildsInfo)
def send_info(call):
    '''Обработка клавиши ДОП ИНФОРМАЦИЯ'''
    user = User(call.message, bot)

    logger.error(f"User {user.id} got additional information {call.data}.")

    # убрать статус ожидания ответа с нажатой кнопки
    bot.answer_callback_query(call.id)
    # удаление нажатой кнопки
    user.EditMessageReplyMarkup()
    # отправка доп. информации
    user.SendMessage(text= BuildsInfo[call.data])