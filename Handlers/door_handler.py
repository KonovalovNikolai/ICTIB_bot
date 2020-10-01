import logging

from Serega.User_Class import User
from Misc import S, B, M
from config import bot

logger = logging.getLogger("Bot.DoorHandler")

@bot.message_handler(func = lambda message: message.text == B.DOORS and
                    User(message).GetUserState() == S.NORMAL)
def send_doors(message):
    user = User(message, bot)
    logger.error(f"User {user.id} got doors.")
    user.SendMessage(text=M.DOORS)