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

STORAGE = {}

list_of_objects = {'Theoretical Foundations of Computer Science': 'B',
                        'Discrete Mathematics': 'C',
                        'Calculus': 'D'
                   }

TABLE_TOI_URL = 'https://docs.google.com/spreadsheets/d/1oBNzC6RDLJyIfWbGGfgmcxoTKvkMIyyQIS3oPsoryN8/edit#gid=0'


@bot.message_handler(func=lambda m: True)
def button_menu(message: Message) -> None:
    markup = ReplyKeyboardMarkup(row_width=4)
    markup.add(KeyboardButton('Theoretical Foundations of Computer Science',
                        'Discrete Mathematics',
                        'Calculus'
                        )
    )
    bot.send_message(
                chat_id=message.from_user.id,
                text="Enter your Surname:",
                reply_markup=markup
    )

    print(message.text)
    if message in list_of_objects:
        STORAGE['user_name'] = message.text
    else:
        STORAGE['object'] = message.text
    ReplyKeyboardRemove()


@bot.message_handler(func=lambda m: True)
def reply_summary(message: Message):
    account = gspread.service_account('key.json')
    sht = account.open_by_url('https://docs.google.com/spreadsheets/d/1oBNzC6RDLJyIfWbGGfgmcxoTKvkMIyyQIS3oPsoryN8/edit#gid=0')
    worksheet = sht.worksheet("Лист1")

    cell = worksheet.find(STORAGE['user_name'])
    correct_cell = list_of_objects[object] + cell[1:]
    val = worksheet.get(correct_cell).first()

    bot.send_message(
        chat_id=message.from_user.id,
        text=val,
    )