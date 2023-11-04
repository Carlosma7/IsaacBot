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
