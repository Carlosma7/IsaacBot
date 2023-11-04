"""
This module provides a Telegram bot for The Binding of Isaac: Rebirth game. It interacts with
users and retrieves information about game elements using the Controller class.

Dependencies:
    - controller: The Controller class for searching and retrieving game element information.
    - template: Templates for generating messages and captions.
    - markups: Markup templates for interactive buttons.
    - run: Functions for generating random runs, spins, and challenges.
    - telebot: The telebot library for Telegram bot functionality.
    - dotenv: The dotenv library for loading environment variables.

Author: Carlos Morales Aguilera
Date: 20-Jun-2023
"""

import os
import telebot
from dotenv import load_dotenv

from controller import Controller
from template import get_element_description
from markups import markup_content, markup_similar
from run import new_run, new_challenge, new_spin

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
    photo = ("https://www.somosxbox.com/wp-content/uploads",
             "/2021/11/The-Binding-of-Isaac-Repentance-scaled.jpg")
    caption = ("Hi! My name is Isaac! \n\nWelcome to The ",
               "Binding of Isaac: Rebirth unofficial bot.")
    bot.send_photo(message.chat.id,
                   photo=photo,
                   caption=caption,
                   parse_mode="Markdown")


@bot.message_handler(commands=['spin'])
def spin(message):
    """
    Handles the /spin command and sends a random spin message.

    Args:
        message (telebot.types.Message): The message object from Telegram.
    """
    bot.send_message(message.chat.id, new_spin(), parse_mode="Markdown")


@bot.message_handler(commands=['run'])
def run(message):
    """
    Handles the /run command and sends a random run message.

    Args:
        message (telebot.types.Message): The message object from Telegram.
    """
    bot.send_message(message.chat.id, new_run(), parse_mode="Markdown")


@bot.message_handler(commands=['challenge'])
def challenge(message):
    """
    Handles the /challenge command and sends a random challenge message.

    Args:
        message (telebot.types.Message): The message object from Telegram.
    """
    bot.send_message(message.chat.id, new_challenge(), parse_mode="Markdown")


@bot.message_handler(commands=['curses'])
def curses(message):
    """
    Handles the /curses command and sends a message with the curses information.

    Args:
        message (telebot.types.Message): The message object from Telegram.
    """
    bot.send_message(message.chat.id,
                     controller.get_curses(),
                     parse_mode="Markdown")


@bot.message_handler(func=lambda message: True)
def query(message):
    """
    Handles user queries and sends information about game elements.

    Args:
        message (telebot.types.Message): The message object from Telegram.
    """
    result, res_type = controller.search_element(message.text)
    if isinstance(result, dict):
        bot.send_photo(message.chat.id,
                       photo=result['image'],
                       caption=get_element_description(result, res_type),
                       parse_mode="Markdown",
                       reply_markup=markup_content(message.text, res_type))
    else:
        bot.send_message(
            message.chat.id,
            f"\"{message.text}\" was not found, but here are some similar possibilities.",
            reply_markup=markup_similar(result))


@bot.callback_query_handler(lambda call: '_' in call.data)
def query_content(call):
    """
    Handles callback queries for retrieving specific content sections of game elements.

    Args:
        call (telebot.types.CallbackQuery): The callback query object from Telegram.
    """
    result = controller.get_element_section(call.data, True)

    bot.send_message(call.message.chat.id, result, parse_mode="Markdown")


@bot.callback_query_handler(lambda call: '_' not in call.data)
def query_similar(call):
    """
    Handles callback queries for retrieving information about similar game elements.

    Args:
        call (telebot.types.CallbackQuery): The callback query object from Telegram.
    """
    caption = (
        "Since we cannot process this item, here is the direct link to ",
        "[Options?](https://bindingofisaacrebirth.fandom.com/wiki/Options%3F)")
    if call.data == 'Options?':
        bot.send_message(call.message.chat.id, caption, parse_mode="Markdown")
    else:
        result, res_type = controller.search_element(call.data, True)
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_photo(call.message.chat.id,
                       photo=result['image'],
                       caption=get_element_description(result, res_type),
                       parse_mode="Markdown",
                       reply_markup=markup_content(call.data, res_type))


bot.polling()
