import logging

from telebot import types

from Serega.User_Class import User
from Misc import B, S, M
from config import bot


def create_kb(vk):
    kb = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(
        text=B.VK1 + "✔️" if vk[0] else B.VK1 + "❌", callback_data="vk1"
    )
    btn2 = types.InlineKeyboardButton(
        text=B.VK2 + "✔️" if vk[1] else B.VK2 + "❌", callback_data="vk2"
    )
    btn3 = types.InlineKeyboardButton(
        text=B.VK3 + "✔️" if vk[2] else B.VK3 + "❌", callback_data="vk3"
    )
    kb.add(btn1, btn2, btn3)
    return kb


@bot.message_handler(
    func=lambda message: message.text == B.FOLLOWS
    and User(message).GetUserState() == S.NORMAL
)
def send_inline_follow_menu(message):
    user = User(message, bot)
    vk = user.GetUserVK()
    user.SendMessage(text=M.VK_SHOW, reply_markup=create_kb(vk))


@bot.callback_query_handler(func=lambda call: call.data.startswith("vk"))
def set_inline_follow(call):
    user = User(call.message, bot)

    user.UpdateVK(call.data)
    vk = user.GetUserVK()
    user.EditMessageReplyMarkup(create_kb(vk))
