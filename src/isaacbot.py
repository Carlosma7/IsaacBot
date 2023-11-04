"""
This module provides a Telegram bot for The Binding of Isaac: Rebirth game. It
interacts with users and retrieves information about game elements using the
Controller class.

Dependencies:
    - controller: The Controller class for searching and retrieving game
    element information.

Author: Carlos Morales Aguilera
Date: 04-Nov-2023
"""

import re
import os
import telebot
from dotenv import load_dotenv

from controller import Controller
from markups import *

load_dotenv(dotenv_path='.env')

TOKEN = os.getenv('TOKEN')

if not TOKEN:
    TOKEN = input('\nPlease enter a valid Telegram Bot Token: ')

bot = telebot.TeleBot(TOKEN)
controller = Controller()


@bot.message_handler(commands=['start'])
def start(message):
    """
    Handles the /start command and sends a welcome message with a photo.

    Args:
        message (telebot.types.Message): The message object from Telegram.
    """
    photo = ("https://media.vandal.net/master/3-2023/20233192354223_1.jpg")
    caption = "Hi! My name is Isaac! \n\nWelcome to The Binding of Isaac: " \
              "Rebirth unofficial bot."
    bot.send_photo(message.chat.id,
                   photo=photo,
                   caption=caption,
                   parse_mode="Markdown")


@bot.message_handler(commands=['achievement'])
def achievement(message):
    """
    Handles the /achievement command and checks the id indicated.

    Args:
        message (telebot.types.Message): The message object from Telegram.
    """
    pattern = r"/achievement (\d+)"
    if not re.match(pattern, message.text) or len(message.text.split()) != 2:
        # Get wrong command message
        reply = controller.get_reply("/achievement", "wrong_command")
        bot.send_message(message.chat.id, text=reply, parse_mode="Markdown")
    else:
        reply = controller.get_achievement(message.text.split()[1])
        bot.send_message(message.chat.id, text=reply, parse_mode="Markdown")

@bot.message_handler(commands=['runes'])
def runes(message):
    """
    Handles the /runes command and returns all available runes in-game.

    Args:
        message (telebot.types.Message): The message object from Telegram.
    """
    if not message.text == '/runes':
        # Get wrong command message
        reply = controller.get_reply("/runes", "wrong_command")
        bot.send_message(message.chat.id, text=reply, parse_mode="Markdown")
    else:
        reply = controller.get_list_runes()
        header = controller.get_reply("/runes", "header")
        bot.send_message(message.chat.id, text=header, parse_mode="Markdown", reply_markup=markup_runes(reply))

@bot.callback_query_handler(lambda call: '\\rune' in call.data)
def rune_content(call):
    """
    Handles callback queries for retrieving specific content from a rune.

    Args:
        call (telebot.types.CallbackQuery): The callback query object from Telegram.
    """
    result = controller.get_rune(call.data.replace('\\rune ', ''))

    bot.send_message(call.message.chat.id, result, parse_mode="Markdown")


bot.polling()
