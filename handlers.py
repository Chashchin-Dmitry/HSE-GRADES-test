import json

import gspread

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

ReplyKeyboardRemove()

TABLE_TOI_URL = 'https://docs.google.com/spreadsheets/d/1oBNzC6RDLJyIfWbGGfgmcxoTKvkMIyyQIS3oPsoryN8/edit#gid=0'


@bot.message_handler(regexp='Theoretical Foundations of Computer Science')
def TOI(message: Message) -> None:
    markup = ReplyKeyboardMarkup(row_width=1)
    markup.add(
        KeyboardButton('Theoretical Foundations of Computer Science'),

    )
    bot.send_message(
                chat_id=message.from_user.id,
                text="Enter your First and Second name:",
                reply_markup=markup
)
    ReplyKeyboardRemove()
    @bot.message_handler(func=lambda m: True)
    def summary_reply(message: Message) -> None:
        account = gspread.service_account(filename='key.json')
        TOI_TABLE = account.open_by_url(TABLE_TOI_URL)
        TOI_TABLE_WORKSHEET = TOI_TABLE.get_worksheet(1)
        cell = TOI_TABLE_WORKSHEET.sheet1.cell(1, 2)
        print(cell.value)


@bot.message_handler(commands=['start'])
def start_bot(message: Message):
    bot.send_message(
        chat_id=message.from_user.id,
        text="Hey! Do you want to see your grades?"
    )