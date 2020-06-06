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

STORAGE = {}

list_of_objects = {'Theoretical Foundations of Computer Science': 'B',
                        'Discrete Mathematics': 'C',
                        'Calculus': 'D'
                   }

TABLE_TOI_URL = 'https://docs.google.com/spreadsheets/d/1oBNzC6RDLJyIfWbGGfgmcxoTKvkMIyyQIS3oPsoryN8/edit#gid=0'

def remove_button(message: Message) -> None:
    remove_markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(chat_id=message.from_user.id,
                     text='Enter your Surname:',
                     reply_markup=remove_markup
                     )


@bot.message_handler(commands=['start'])
def button_menu(message: Message) -> None:
    markup = ReplyKeyboardMarkup(row_width=4)
    TOI_BUTTON = types.KeyboardButton('Theoretical Foundations of Computer Science')
    DISC_BUTTON = types.KeyboardButton('Discrete Mathematics')
    CALC_BUTTON = types.KeyboardButton('Calculus')
    markup.add(TOI_BUTTON, DISC_BUTTON, CALC_BUTTON)
    bot.send_message(
                chat_id=message.from_user.id,
                text="Main menu:",
                reply_markup=markup
    )
    #STORAGE['object'] = message.text
    #with open('json.json', 'w'):
     #   json_var = json.dumps(STORAGE)


@bot.message_handler(func=lambda message: True)
def remove_button(message: Message) -> False:
    remove_markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(chat_id=message.from_user.id,
                     text='Enter your Surname:',
                     reply_markup=remove_markup
                     )


@bot.message_handler(func=lambda message: True)
def reply_summary(message: Message) -> None:
    STORAGE['user_name'] = message.text
    print(STORAGE)
    account = gspread.service_account('key.json')
    sht = account.open_by_url('https://docs.google.com/spreadsheets/d/1oBNzC6RDLJyIfWbGGfgmcxoTKvkMIyyQIS3oPsoryN8/edit#gid=0')
    worksheet = sht.worksheet("Лист1")

    cell = worksheet.find(STORAGE['user_name'])
    correct_cell = list_of_objects[STORAGE['object']] + cell[1:]
    val = worksheet.get(correct_cell).first()

    bot.send_message(
        chat_id=message.from_user.id,
        text=val,
    )
