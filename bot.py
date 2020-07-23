import logging
from config import bot
import handlers

def main():
    logger = logging.getLogger('Bot')

    # Create handlers
    f_handler = logging.FileHandler(filename='Logs/botlog.log', mode='w')
    f_handler.setLevel(logging.INFO)

    # Create formatters and add it to handlers
    f_format = logging.Formatter( fmt= '%(asctime)s - %(name)s - %(funcName)s: %(message)s',
                                datefmt= '%d-%M-%Y %H:%M:%S')
    f_handler.setFormatter(f_format)

    # Add handlers to the logger
    logger.addHandler(f_handler)

    logger.error('Bot started')
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logger.Exception("Fail:")

if __name__ == "__main__":
    main()