"""
This module provides a class for creating markups using the Telebot library.

The markups are used in a Telegram bot to generate interactive keyboards for
selecting options or content.

Note: The functions in this module require the Telebot library to be installed.

Author: Carlos Morales Aguilera
Date: 04-Nov-2023
"""


import telebot

# Disable too few public methods warning, since it will grow in the future, but
# just to pass pylint checks now
# pylint: disable=R0903


class Markup:
    """
    This class provides methods for creating markups using the Telebot library.
    The markups are used in a Telegram bot to generate interactive keyboards
    for selecting options or content.
    """

    @staticmethod
    def markup_entity(entity, values):
        """
        Create a markup for choosing values of an entity.

        Args:
            entity (str): A str containing the entity type.
            values (list): A list of elements to display as buttons.

        Returns:
            telebot.types.InlineKeyboardMarkup: Markup for selecting similar
            elements.
        """
        markup = telebot.types.InlineKeyboardMarkup(row_width=1)

        for value in values:
            button = telebot.types.InlineKeyboardButton(
                value, callback_data=f"/{entity} {value}")
            markup.add(button)

        return markup

    @staticmethod
    def markup_similar(similarities):
        """
        Create a markup for choosing similar elements.

        Args:
            similarities (list): A list of elements to display as buttons.

        Returns:
            telebot.types.InlineKeyboardMarkup: Markup for selecting similar
            elements.
        """
        markup = telebot.types.InlineKeyboardMarkup(row_width=1)

        for elem in similarities:
            button = telebot.types.InlineKeyboardButton(
                elem, callback_data=elem)
            markup.add(button)

        return markup

    @staticmethod
    def markup_content(elem):
        """
        Create a markup based on the element type.

        Args:
            elem (str): The name or identifier of the element.

        Returns:
            telebot.types.InlineKeyboardMarkup or False: Markup for the
            specified element type,
            or False if not supported.
        """
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)

        bt1 = telebot.types.InlineKeyboardButton(
            'Effects', callback_data=f"Effects_{elem}")
        bt2 = telebot.types.InlineKeyboardButton(
            'Notes', callback_data=f"Notes_{elem}")
        bt3 = telebot.types.InlineKeyboardButton(
            'Synergies', callback_data=f"Synergies_{elem}")
        bt4 = telebot.types.InlineKeyboardButton(
            'Interactions',
            callback_data=f"Interactions_{elem}")

        markup.add(bt1, bt2, bt3, bt4)

        return markup
