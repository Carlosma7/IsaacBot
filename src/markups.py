"""
This module provides a class for creating markups using the Telebot library.

The markups are used in a Telegram bot to generate interactive keyboards for
selecting options or content.

Note: The functions in this module require the Telebot library to be installed.

Author: Carlos Morales Aguilera
Date: 04-Nov-2023
"""


import telebot


class Markup:
    """
    This class provides methods for creating markups using the Telebot library.
    The markups are used in a Telegram bot to generate interactive keyboards
    for selecting options or content.
    """

    @staticmethod
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
                rune, callback_data=f"/rune {rune}")
            markup.add(button)

        return markup

    @staticmethod
    def markup_pickups(pickups):
        """
        Create a markup for choosing pickups.

        Args:
            pickups (list): A list of elements to display as buttons.

        Returns:
            telebot.types.InlineKeyboardMarkup: Markup for selecting similar
            elements.
        """
        markup = telebot.types.InlineKeyboardMarkup(row_width=1)

        for pickup in pickups:
            button = telebot.types.InlineKeyboardButton(
                pickup, callback_data=f"/pickup {pickup}")
            markup.add(button)

        return markup

    @staticmethod
    def markup_soulstones(soulstones):
        """
        Create a markup for choosing soul stones.

        Args:
            soulstones (list): A list of elements to display as buttons.

        Returns:
            telebot.types.InlineKeyboardMarkup: Markup for selecting similar
            elements.
        """
        markup = telebot.types.InlineKeyboardMarkup(row_width=1)

        for soulstone in soulstones:
            button = telebot.types.InlineKeyboardButton(
                soulstone, callback_data=f"/soulstone {soulstone}")
            markup.add(button)

        return markup
