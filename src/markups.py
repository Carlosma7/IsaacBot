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
