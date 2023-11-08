"""
This file provides a class for handling pills in the game.

Author: Carlos Morales Aguilera
Date: 04-Nov-2023
"""


class Pill:
    """
    Represents a pill in the game.

    Attributes:
        __name (str): The name of the pill.
    """

    def __init__(self, name: str):
        """
        Initializes a new instance of the Pill class.

        Args:
            __name (str): The name of the pill.
        """
        self.__name = name

    @staticmethod
    def to_str(pill):
        """
        Convert a pill to a formatted string representation.

        Args:
            pill (dict): A dictionary representing a pill with
            'name', 'effect' and 'horse_effect' keys.

        Returns:
            str: A formatted string representation of the pill,
            including its name, effect and horse_effect.
        """
        item_values = []

        # Add name
        item_values.append(f"*{pill.get('name')}*.")

        # Add effect
        item_values.append(f"*Effect*: {pill.get('effect')}")

        # Add horse_effect
        item_values.append(f"*Horse effect*: {pill.get('horse_effect')}")

        return "\n\n".join(item_values)

    def get_list_elements(self, database):
        """
        Retrieve a list of pill names from the provided database.

        Args:
            database: A database object with a Pills collection.

        Returns:
            A list of pill names extracted from the Pills collection in the
            database.
        """
        pills = database.Pills.find({})
        return [pill.get('name') for pill in pills]

    def get_element(self, database):
        """
        Retrieves the description and details of the pill.

        Returns:
            str: Description and details of the pill
        """
        pill = database.Pills.find_one({"name": self.__name})
        return self.to_str(pill)
