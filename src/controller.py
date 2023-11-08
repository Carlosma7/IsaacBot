"""
This module provides a controller class for searching and retrieving
information about different game elements, including items, trinkets,
cards/runes, pills, and transformations.

Author: Carlos Morales Aguilera
Date: 04-Nov-2023
"""

# Disable order due to error with pylint, but the order will
# still be respected.
# pylint: disable=C0411

import os
import pymongo
from dotenv import load_dotenv

from achievements import Achievement
from cards import Card
from challenges import Challenge
from characters import Character
from curses import Curse
from pickups import Pickup
from pills import Pill
from runes import Rune
from soulstones import SoulStone
from transformations import Transformation

load_dotenv(dotenv_path='.env')

MONGO_TOKEN = os.getenv('MONGO_TOKEN')
if not MONGO_TOKEN:
    MONGO_TOKEN = input('\nPlease enter a valid MongoDB Atlas Token: ')

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
    def __init__(self):
        """
        Initializes an instance of a class with a dictionary that maps element
        types to their respective classes.

        The `element_types` dictionary associates strings representing
        different types of in-game elements with their corresponding class
        definitions. This is useful for managing and organizing various
        game-related data, such as achievements, pickups, runes, soulstones,
        decks, curses, pills, transformations, challenges, and characters.

        Parameters:
        - self: The instance of the class to be initialized.
        """
        self.element_types = {
            'achievements': Achievement,
            'pickups': Pickup,
            'runes': Rune,
            'soulstones': SoulStone,
            'cards': Card,
            'curses': Curse,
            'pills': Pill,
            'transformations': Transformation,
            'challenges': Challenge,
            'characters': Character
        }

    def get_list_elements(self, elem_type, deck=False):
        """
        Get a list of elements of a specified type from the database.

        Args:
            elem_type (str): The type of elements to retrieve.
            deck (bool, optional): Whether to retrieve elements associated with
            a deck.
                Defaults to False.

        Returns:
            list: A list of elements of the specified type.
        """
        element = self.element_types[elem_type]('List')
        if deck:
            elements = element.get_list_elements(database, deck)
            return elements
        elements = element.get_list_elements(database)
        return elements

    def get_element(self, elem_type, elem_id):
        """
        Get a specific element of a specified type from the database.

        Args:
            elem_type (str): The type of element to retrieve.
            elem_id: The unique identifier of the element.

        Returns:
            object: The retrieved element.
        """
        element = self.element_types[elem_type](elem_id)
        result = element.get_element(database)
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
