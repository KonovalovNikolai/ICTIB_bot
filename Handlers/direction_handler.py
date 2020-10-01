import logging

from Serega.User_Class import User
from Misc import S, B, M
from config import bot

logger = logging.getLogger('Bot.DirectHandler')

@bot.message_handler(func = lambda message: message.text == B.DIRECTION and
                    User(message).GetUserState() == S.NORMAL)
def send_directions(message):
    user = User(message, bot)
    logger.error(f"User {user.id} got directions url.")
    # отправка направлений
    user.SendMessage(text='http://abit.ictis.sfedu.ru/bachelor.html#directions', raw=False)