import json

import gspread

import re

from telebot import types
from telebot.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
)

from preparation import bot

STORAGE = {'object': '', 'user_name': ''}

list_of_objects = {'Theoretical Foundations of Computer Science': 'B',
                        'Discrete Mathematics': 'C',
                        'Calculus': 'D'
                   }


SURNAME_STORAGE = {}
with open('json.json', 'r') as f:
    SURNAME_STORAGE = json.load(f)
print(SURNAME_STORAGE)

@bot.message_handler(func= lambda message: True)
def button_menu(message: Message) -> None:
    markup = ReplyKeyboardMarkup(row_width=4)
    TOI_BUTTON = types.KeyboardButton('Theoretical Foundations of Computer Science')
    DISC_BUTTON = types.KeyboardButton('Discrete Mathematics')
    CALC_BUTTON = types.KeyboardButton('Calculus')
    markup.add(TOI_BUTTON, DISC_BUTTON, CALC_BUTTON)

    if message.text in list_of_objects or message.text in SURNAME_STORAGE or STORAGE['object']:
        if message.text in list_of_objects:
            STORAGE['object'] = message.text
            remove_markup = types.ReplyKeyboardRemove(selective=False)
            bot.send_message(chat_id=message.from_user.id,
                             text='Enter your Surname(russian):',
                             reply_markup=remove_markup
                             )
            return None

        replace_message = message.text
        for matching_name in SURNAME_STORAGE:
            if replace_message.lower() == matching_name.lower():
                STORAGE['user_name'] = matching_name
            else:
                pass

        if STORAGE['user_name'] not in SURNAME_STORAGE:
            bot.send_message(chat_id=message.from_user.id,
                             text="Can not find your surname!"
                             )
            return bot.send_message(
                chat_id=message.from_user.id,
                text="Main menu:",
                reply_markup=markup
            )

        if STORAGE['user_name']:
            account = gspread.service_account('key.json')
            url = account.open_by_url('https://docs.google.com/spreadsheets/d/1oBNzC6RDLJyIfWbGGfgmcxoTKvkMIyyQIS3oPsoryN8/edit#gid=0')
            worksheet = url.worksheet("Лист1")

            surname_re = re.compile(STORAGE['user_name'])
            object_re = re.compile(STORAGE['object'])
            surname_cell = worksheet.find(surname_re)
            object_cell = worksheet.find(object_re)
            surname_cell_value = surname_cell.row
            object_cell_value = object_cell.col

            val = worksheet.cell(surname_cell_value, object_cell_value).value

            bot.send_message(
                chat_id=message.from_user.id,
                text=val,
            )
            STORAGE['user_name'] = ''
            STORAGE['object'] = ''
            bot.send_message(
                chat_id=message.from_user.id,
                text="Main menu:",
                reply_markup=markup
            )
    else:
        bot.send_message(
            chat_id=message.from_user.id,
            text="Main menu:",
            reply_markup=markup
        )
