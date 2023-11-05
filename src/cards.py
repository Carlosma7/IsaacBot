"""
This file provides a class for handling cards in the game.

Author: Carlos Morales Aguilera
Date: 04-Nov-2023
"""

from collections import OrderedDict


class Card:
    """
    Represents a card in the game.

    Attributes:
        __name (str): The name of the card.
    """

    def __init__(self, name: str):
        """
        Initializes a new instance of the Card class.

        Args:
            __name (str): The name of the card.
        """
        self.__name = name

    @staticmethod
    def to_str(card):
        """
        Convert a card to a formatted string representation.

        Args:
            card (dict): A dictionary representing a card with
            'name', 'unlock', 'message', and 'effect' keys.

        Returns:
            str: A formatted string representation of the card,
            including its name, unlock method, description and effects.
        """
        item_values = []

        # Add name
        item_values.append(f"*{card.get('name')}*.")

        # Add description
        item_values.append(f"_{card.get('message')}_.")

        # Add unlock method
        item_values.append(f"Unlock: {card.get('unlock')}.")

        # Add effects
        item_values.append(f"{card.get('effect')}")

        return "\n\n".join(item_values)

    def get_list_decks(self, database):
        """
        Retrieve a list of unique 'deck' values from the provided database.

        Args:
            database: A database object with a Cards collection.

        Returns:
            list: A list of unique 'deck' values found in the collection.
        """
        cards = database.Cards.find({})
        decks = OrderedDict()
        for card in cards:
            deck = card.get('deck')
            if deck is not None:
                decks[deck] = None

        return list(decks.keys())

    def get_list_cards_in_deck(self, database, deck):
        """
        Retrieve a list of card names in a deck from the provided database.

        Args:
            database: A database object with a Cards collection.

        Returns:
            A list of cards names in a deck extracted from the Cards collection
            in the database.
        """
        cards = database.Cards.find({'deck': deck})
        return [card.get('name') for card in cards]

    def get_card(self, database):
        """
        Retrieves the description and details of the card.

        Returns:
            str: Description and details of the card
        """
        card = database.Cards.find_one({"name": self.__name})
        return self.to_str(card)
