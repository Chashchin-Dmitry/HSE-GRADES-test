import logging


import handlers

from preparation import bot

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    bot.polling()