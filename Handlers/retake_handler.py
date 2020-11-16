import logging

from Serega.User_Class import User
from Misc import S, B, M
from config import bot

logger = logging.getLogger("Bot.RetakeHandler")

@bot.message_handler(func = lambda message: message.text == B.RETAKE and
                    User(message).GetUserState() == S.NORMAL)
def Send_Retake(message):
    user = User(message, bot)
    user.SendMessage(text=M.RETAKE)
    logger.error(f"User {user.id} got a retake url.")