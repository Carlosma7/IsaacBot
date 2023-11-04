"""
This module provides a controller class for searching and retrieving
information about different game elements, including items, trinkets,
cards/runes, pills, and transformations.

Author: Carlos Morales Aguilera
Date: 04-Nov-2023
"""

import os
import pymongo
from dotenv import load_dotenv

from achievements import Achievement
from pickups import Pickup
from runes import Rune

load_dotenv(dotenv_path='.env')

MONGO_TOKEN = os.getenv('MONGO_TOKEN')
if not MONGO_TOKEN:
    MONGO_TOKEN = input('\nPlease enter a valid Telegram Bot Token: ')

client = pymongo.MongoClient(MONGO_TOKEN, serverSelectionTimeoutMS=2000)
database = client.Isaac


class Controller:
    """
    The Controller class handles the searching and retrieval of game element
    information.

    Methods:
        - get_achievement(number): Retrieves the info of a specific
        achievement.
    """

    def get_achievement(self, number):
        """
        Retrieve information about a specific achievement by its number.

        Args:
            number (int): The unique identifier (number) of the achievement to
            retrieve.

        Returns:
            str: If a valid achievement with the specified number is found,
            returns a str containing achievement details. If the achievement
            number is not valid (outside the range 1 to 637), returns a string
            indicating that the achievement ID is not valid.
        """
        achievement = Achievement(number)
        result = achievement.get_achievement(database)
        if result:
            return result

        return "Achievement ID is not valid, achievement ID must be between " \
               "1 and 637."

    def get_list_pickups(self):
        """
        Get a list of available pickups from the database.

        Returns:
            list: A list of pickup names from the database.
        """
        pickup = Pickup('LIST')
        pickups = pickup.get_list_pickups(database)
        return pickups

    def get_pickup(self, name):
        """
        Get detailed information about a specific pickup.

        Args:
        name (str): The name of the pickup to retrieve.

        Returns:
            dict: A dictionary containing information about the specified
            pickup.
        """
        pickup = Pickup(name)
        result = pickup.get_pickup(database)
        return result

    def get_list_runes(self):
        """
        Get a list of available runes from the database.

        Returns:
            list: A list of rune names from the database.
        """
        rune = Rune('LIST')
        runes = rune.get_list_runes(database)
        return runes

    def get_rune(self, name):
        """
        Get detailed information about a specific rune.

        Args:
        name (str): The name of the rune to retrieve.

        Returns:
            dict: A dictionary containing information about the specified rune.
        """
        rune = Rune(name)
        result = rune.get_rune(database)
        return result

    def get_reply(self, command, reply_type):
        """
        Get a reply message based on a command and reply type.

        Args:
        command (str): The command to which the reply is associated.
        reply_type (str): The type of the reply (e.g., 'wrong_command',
        'header').

        Returns:
            str: The reply message associated with the given command and reply
            type.
        """
        reply = database.Replies.find_one({
            "command": command,
            "type": reply_type,
            })
        return reply.get('message').encode('utf-8').decode('unicode_escape')
