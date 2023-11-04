"""
This file provides a class for handling runes in the game.

Author: Carlos Morales Aguilera
Date: 04-Nov-2023
"""


class Rune:
    """
    Represents a rune in the game.

    Attributes:
        __name (str): The name of the rune.
    """

    def __init__(self, name: str):
        """
        Initializes a new instance of the Rune class.

        Args:
            __name (str): The name of the rune.
        """
        self.__name = name

    @staticmethod
    def to_str(rune):
        """
        Convert a rune to a formatted string representation.

        Args:
            rune (dict): A dictionary representing a rune with
            'name', 'unlock', 'message', and 'effect' keys.

        Returns:
            str: A formatted string representation of the rune,
            including its name, unlock method, description and effects.
        """
        item_values = []

        # Add name
        item_values.append(f"*{rune.get('name')}*.")

        # Add description
        item_values.append(f"_{rune.get('message')}_.")

        # Add unlock method
        item_values.append(f"Unlock: {rune.get('unlock')}.")

        # Add effects
        item_values.append(f"{rune.get('effect')}")

        return "\n\n".join(item_values)

    def get_list_runes(self, database):
        """
        Retrieve a list of rune names from the provided database.

        Args:
            database: A database object with a Runes collection.

        Returns:
            A list of rune names extracted from the Runes collection in the
            database.
        """
        runes = database.Runes.find({})
        return [rune.get('name') for rune in runes]

    def get_rune(self, database):
        """
        Retrieves the description and details of the rune.

        Returns:
            str: Description and details of the rune
        """
        rune = database.Runes.find_one({"name": self.__name})
        return self.to_str(rune)
