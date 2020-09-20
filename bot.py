import logging

import Handlers
from config import bot


def main():
    logger = logging.getLogger("Bot")

    # Create handlers
    f_handler = logging.FileHandler(filename="Logs/botlog.log", mode="w")
    f_handler.setLevel(logging.ERROR)

    # Create formatters and add it to handlers
    f_format = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(funcName)s: %(message)s",
        datefmt="%d-%M-%Y %H:%M:%S",
    )
    f_handler.setFormatter(f_format)

    # Add handlers to the logger
    logger.addHandler(f_handler)

    logger.error("Bot started")

    bot.polling(none_stop=True)


if __name__ == "__main__":
    main()
