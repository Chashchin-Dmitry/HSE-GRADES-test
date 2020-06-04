import telebot
from telebot import apihelper

import config

bot = telebot.TeleBot(token=config.TOKEN)
apihelper.proxy = config.PROXY