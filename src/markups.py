"""
This module provides functions for creating markups using the Telebot library.

The markups are used in a Telegram bot to generate interactive keyboards for
selecting options or content.

Functions:
- markup_runes(runens): Create a markup for choosing a rune.


Note: The functions in this module require the Telebot library to be installed.

Author: Carlos Morales Aguilera
Date: 04-Nov-2023
"""

import telebot


def markup_runes(runes):
    """
    Create a markup for choosing runes.

    Args:
        runes (list): A list of elements to display as buttons.

    Returns:
        telebot.types.InlineKeyboardMarkup: Markup for selecting similar
        elements.
    """
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)

    for rune in runes:
        button = telebot.types.InlineKeyboardButton(
            rune, callback_data=f"\\rune {rune}")
        markup.add(button)

    return markup
