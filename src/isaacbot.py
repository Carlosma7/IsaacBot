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
from markups import Markup

load_dotenv(dotenv_path='.env')

TOKEN = os.getenv('TOKEN')

if not TOKEN:
    TOKEN = input('\nPlease enter a valid Telegram Bot Token: ')

bot = telebot.TeleBot(TOKEN)
controller = Controller()
markup = Markup()


@bot.message_handler(commands=['start'])
def start(message):
    """
    Handles the /start command and sends a welcome message with a photo.

    Args:
        message (telebot.types.Message): The message object from Telegram.
    """
    photo = "https://media.vandal.net/master/3-2023/20233192354223_1.jpg"
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


@bot.message_handler(commands=['pickups'])
def pickups(message):
    """
    Handles the /pickups command and returns all available pickups in-game.

    Args:
        message (telebot.types.Message): The message object from Telegram.
    """
    if not message.text == '/pickups':
        # Get wrong command message
        reply = controller.get_reply("/pickups", "wrong_command")
        bot.send_message(message.chat.id, text=reply, parse_mode="Markdown")
    else:
        reply = controller.get_list_pickups()
        header = controller.get_reply("/pickups", "header")
        bot.send_message(
            message.chat.id, text=header,
            parse_mode="Markdown", reply_markup=markup.markup_pickups(reply))


@bot.callback_query_handler(lambda call: '/pickup' in call.data)
def pickup_content(call):
    """
    Handles callback queries for retrieving specific content from a pickup.

    Args:
        call (telebot.types.CallbackQuery): The callback query object from
        Telegram.
    """
    result = controller.get_pickup(call.data.replace('/pickup ', ''))

    bot.delete_message(call.message.chat.id, call.message.id)
    bot.send_message(call.message.chat.id, result, parse_mode="Markdown")


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
        bot.send_message(
            message.chat.id, text=header,
            parse_mode="Markdown", reply_markup=markup.markup_runes(reply))


@bot.callback_query_handler(lambda call: '/rune' in call.data)
def rune_content(call):
    """
    Handles callback queries for retrieving specific content from a rune.

    Args:
        call (telebot.types.CallbackQuery): The callback query object from
        Telegram.
    """
    result = controller.get_rune(call.data.replace('/rune ', ''))

    bot.delete_message(call.message.chat.id, call.message.id)
    bot.send_message(call.message.chat.id, result, parse_mode="Markdown")


@bot.message_handler(commands=['soulstones'])
def soulstones(message):
    """
    Handles the /soulstones command and returns all available soul stones
    in-game.

    Args:
        message (telebot.types.Message): The message object from Telegram.
    """
    if not message.text == '/soulstones':
        # Get wrong command message
        reply = controller.get_reply("/soulstones", "wrong_command")
        bot.send_message(message.chat.id, text=reply, parse_mode="Markdown")
    else:
        reply = controller.get_list_soulstones()
        header = controller.get_reply("/soulstones", "header")
        bot.send_message(
            message.chat.id, text=header,
            parse_mode="Markdown",
            reply_markup=markup.markup_soulstones(reply))


@bot.callback_query_handler(lambda call: '/soulstone' in call.data)
def soulstone_content(call):
    """
    Handles callback queries for retrieving specific content from a soul stone.

    Args:
        call (telebot.types.CallbackQuery): The callback query object from
        Telegram.
    """
    result = controller.get_soulstone(call.data.replace('/soulstone ', ''))

    bot.delete_message(call.message.chat.id, call.message.id)
    bot.send_message(call.message.chat.id, result, parse_mode="Markdown")


@bot.message_handler(commands=['cards'])
def cards(message):
    """
    Handles the /cards command and returns all available cards in-game.

    Args:
        message (telebot.types.Message): The message object from Telegram.
    """
    if not message.text == '/cards':
        # Get wrong command message
        reply = controller.get_reply("/cards", "wrong_command")
        bot.send_message(message.chat.id, text=reply, parse_mode="Markdown")
    else:
        reply = controller.get_list_decks()
        header = controller.get_reply("/cards", "header")
        bot.send_message(
            message.chat.id, text=header,
            parse_mode="Markdown",
            reply_markup=markup.markup_decks(reply))


@bot.callback_query_handler(lambda call: '/deck' in call.data)
def deck_content(call):
    """
    Handles callback queries for retrieving specific content from a deck.

    Args:
        call (telebot.types.CallbackQuery): The callback query object from
        Telegram.
    """
    reply = controller.get_list_cards_in_deck(call.data.replace('/deck ', ''))
    header = f"*{call.data.replace('/deck ', '')}* deck."

    bot.delete_message(call.message.chat.id, call.message.id)
    bot.send_message(
            call.message.chat.id, text=header,
            parse_mode="Markdown",
            reply_markup=markup.markup_cards(reply))


@bot.callback_query_handler(lambda call: '/card' in call.data)
def card_content(call):
    """
    Handles callback queries for retrieving specific content from a card.

    Args:
        call (telebot.types.CallbackQuery): The callback query object from
        Telegram.
    """
    result = controller.get_card(call.data.replace('/card ', ''))

    bot.delete_message(call.message.chat.id, call.message.id)
    bot.send_message(call.message.chat.id, result, parse_mode="Markdown")


@bot.message_handler(commands=['curses'])
def curses(message):
    """
    Handles the /curses command and returns all available curses
    in-game.

    Args:
        message (telebot.types.Message): The message object from Telegram.
    """
    if not message.text == '/curses':
        # Get wrong command message
        reply = controller.get_reply("/curses", "wrong_command")
        bot.send_message(message.chat.id, text=reply, parse_mode="Markdown")
    else:
        reply = controller.get_list_curses()
        header = controller.get_reply("/curses", "header")
        bot.send_message(
            message.chat.id, text=header,
            parse_mode="Markdown",
            reply_markup=markup.markup_curses(reply))


@bot.callback_query_handler(lambda call: '/curse' in call.data)
def curse_content(call):
    """
    Handles callback queries for retrieving specific content from a curse.

    Args:
        call (telebot.types.CallbackQuery): The callback query object from
        Telegram.
    """
    result = controller.get_curse(call.data.replace('/curse ', ''))

    bot.delete_message(call.message.chat.id, call.message.id)
    bot.send_message(call.message.chat.id, result, parse_mode="Markdown")


@bot.message_handler(commands=['pills'])
def pills(message):
    """
    Handles the /pills command and returns all available pills
    in-game.

    Args:
        message (telebot.types.Message): The message object from Telegram.
    """
    if not message.text == '/pills':
        # Get wrong command message
        reply = controller.get_reply("/pills", "wrong_command")
        bot.send_message(message.chat.id, text=reply, parse_mode="Markdown")
    else:
        reply = controller.get_list_pills()
        header = controller.get_reply("/pills", "header")
        bot.send_message(
            message.chat.id, text=header,
            parse_mode="Markdown",
            reply_markup=markup.markup_pills(reply))


@bot.callback_query_handler(lambda call: '/pill' in call.data)
def pill_content(call):
    """
    Handles callback queries for retrieving specific content from a pill.

    Args:
        call (telebot.types.CallbackQuery): The callback query object from
        Telegram.
    """
    result = controller.get_pill(call.data.replace('/pill ', ''))

    bot.delete_message(call.message.chat.id, call.message.id)
    bot.send_message(call.message.chat.id, result, parse_mode="Markdown")


bot.polling()
