"""
This module provides functions for creating markups using the Telebot library.

The markups are used in a Telegram bot to generate interactive keyboards for selecting
options or content.

Functions:
- markup_similar(similarities): Create a markup for choosing similar elements.
- markup_item_trinket(elem, elem_type): Create a markup for choosing content options
for an item or trinket.
- markup_content(elem, elem_type): Create a markup based on the element type.

Note: The functions in this module require the Telebot library to be installed.

Author: Carlos Morales Aguilera
Date: 20-Jun-2023
"""

import telebot


def markup_similar(similarities):
    """
    Create a markup for choosing similar elements.

    Args:
        similarities (list): A list of elements to display as buttons.

    Returns:
        telebot.types.InlineKeyboardMarkup: Markup for selecting similar elements.
    """
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)

    for elem in similarities:
        button = telebot.types.InlineKeyboardButton(elem, callback_data=elem)
        markup.add(button)

    return markup


def markup_item_trinket(elem, elem_type):
    """
    Create a markup for choosing content options for an item or trinket.

    Args:
        elem (str): The name or identifier of the element.
        elem_type (str): The type of the element (e.g., 'Item', 'Trinket').

    Returns:
        telebot.types.InlineKeyboardMarkup: Markup for selecting content options.
    """
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)

    bt1 = telebot.types.InlineKeyboardButton(
        'Effects', callback_data=f"Effects_{elem_type}_{elem}")
    bt2 = telebot.types.InlineKeyboardButton(
        'Notes', callback_data=f"Notes_{elem_type}_{elem}")
    bt3 = telebot.types.InlineKeyboardButton(
        'Synergies', callback_data=f"Synergies_{elem_type}_{elem}")
    bt4 = telebot.types.InlineKeyboardButton(
        'Interactions',
        callback_data=f"Interactions_{elem_type}_{elem}")

    markup.add(bt1, bt2, bt3, bt4)

    return markup


def markup_content(elem, elem_type):
    """
    Create a markup based on the element type.

    Args:
        elem (str): The name or identifier of the element.
        elem_type (str): The type of the element.

    Returns:
        telebot.types.InlineKeyboardMarkup or False: Markup for the specified element type,
        or False if not supported.
    """
    if elem_type in ['Item', 'Trinket']:
        return markup_item_trinket(elem, elem_type)
    return False
