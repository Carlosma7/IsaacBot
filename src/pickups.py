"""
This file provides a class for handling pickups in the game.

Author: Carlos Morales Aguilera
Date: 04-Nov-2023
"""


class Pickup:
    """
    Represents a pickup in the game.

    Attributes:
        __name (str): The name of the pickup.
    """

    def __init__(self, name: str):
        """
        Initializes a new instance of the Pickup class.

        Args:
            __name (str): The name of the pickup.
        """
        self.__name = name

    @staticmethod
    def to_str(pickup):
        """
        Convert a pickup to a formatted string representation.

        Args:
            pickup (dict): A dictionary representing a pickup with
            'name', 'unlock', 'message', and 'effect' keys.

        Returns:
            str: A formatted string representation of the pickup,
            including its name, unlock method, description and effects.
        """
        item_values = []

        # Add name
        item_values.append(f"*{pickup.get('name')}*.")

        # Add description
        item_values.append(f"_{pickup.get('message')}_.")

        # Add unlock method
        item_values.append(f"Unlock: {pickup.get('unlock')}.")

        # Add effects
        item_values.append(f"{pickup.get('effect')}")

        return "\n\n".join(item_values)

    def get_list_elements(self, database):
        """
        Retrieve a list of pickup names from the provided database.

        Args:
            database: A database object with a Pickups collection.

        Returns:
            A list of pickup names extracted from the Pickups collection in the
            database.
        """
        pickups = database.Pickups.find({})
        return [pickup.get('name') for pickup in pickups]

    def get_element(self, database):
        """
        Retrieves the description and details of the pickup.

        Returns:
            str: Description and details of the pickup
        """
        pickup = database.Pickups.find_one({"name": self.__name})
        return self.to_str(pickup)
