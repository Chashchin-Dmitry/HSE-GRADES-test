import json

from telebot import types
from telebot.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardRemove,
)

from preparation import bot

from config import TOKEN

markup = types.ReplyKeyboardMarkup(row_width=1)
@bot.message_handler(commands='Theoretical Foundations of Computer Science')
def hello(message: Message) -> None:
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(TOKEN,message, reply_markup=markup)
    TOI = types.KeyboardButton('Theoretical Foundations of Computer Science')
    markup.add(TOI)
    bot.send_message(
                chat_id=message.from_user.id,
                text="Start",
                markup=markup
)
