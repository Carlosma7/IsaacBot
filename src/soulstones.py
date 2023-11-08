"""
This file provides a class for handling soul stones in the game.

Author: Carlos Morales Aguilera
Date: 05-Nov-2023
"""


class SoulStone:
    """
    Represents a soul stone in the game.

    Attributes:
        __name (str): The name of the soul stone.
    """

    def __init__(self, name: str):
        """
        Initializes a new instance of the Soulstone class.

        Args:
            __name (str): The name of the soul stone.
        """
        self.__name = name

    @staticmethod
    def to_str(soulstone):
        """
        Convert a soul stone to a formatted string representation.

        Args:
            soulstone (dict): A dictionary representing a soul stone with
            'name', 'unlock', 'message', and 'effect' keys.

        Returns:
            str: A formatted string representation of the soul stone,
            including its name, unlock method, description and effects.
        """
        item_values = []

        # Add name
        item_values.append(f"*{soulstone.get('name')}*.")

        # Add description
        item_values.append(f"_{soulstone.get('message')}_.")

        # Add unlock method
        item_values.append(f"Unlock: {soulstone.get('unlock')}.")

        # Add effects
        item_values.append(f"{soulstone.get('effect')}")

        return "\n\n".join(item_values)

    def get_list_elements(self, database):
        """
        Retrieve a list of soul stone names from the provided database.

        Args:
            database: A database object with a SoulStone collection.

        Returns:
            A list of soul stone names extracted from the Soulstones
            collection in the database.
        """
        soulstones = database.SoulStones.find({})
        return [soulstone.get('name') for soulstone in soulstones]

    def get_element(self, database):
        """
        Retrieves the description and details of the soulstone.

        Returns:
            str: Description and details of the soulstone
        """
        soulstone = database.SoulStones.find_one({"name": self.__name})
        return self.to_str(soulstone)
