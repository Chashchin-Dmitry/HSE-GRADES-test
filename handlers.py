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

STORAGE = {'object': '', 'user_name': ''}

list_of_objects = {'Theoretical Foundations of Computer Science': 'B',
                        'Discrete Mathematics': 'C',
                        'Calculus': 'D'
                   }

TABLE_TOI_URL = 'https://docs.google.com/spreadsheets/d/1oBNzC6RDLJyIfWbGGfgmcxoTKvkMIyyQIS3oPsoryN8/edit#gid=0'

SURNAME_STORAGE = {}
with open('json.json', 'r') as f:
    SURNAME_STORAGE = json.load(f)

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
    #with open('json.json', 'w'):
     #   json_var = json.dumps(STORAGE)
    if message.text in list_of_objects:
        STORAGE['object'] = message.text
        remove_markup = types.ReplyKeyboardRemove(selective=False)
        bot.send_message(chat_id=message.from_user.id,
                         text='Enter your Surname:',
                         reply_markup=remove_markup
                         )
    elif message.text in SURNAME_STORAGE:
        STORAGE['user_name'] = message.text
    else:
        pass


#json_STORAGE = json.dumps(STORAGE['object'])

    print(STORAGE)
    if message.text == STORAGE['user_name']:
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
