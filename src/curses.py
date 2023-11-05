"""
This file provides a class for handling curses in the game.

Author: Carlos Morales Aguilera
Date: 05-Nov-2023
"""


class Curse:
    """
    Represents a curse in the game.

    Attributes:
        __name (str): The name of the curse.
    """

    def __init__(self, name: str):
        """
        Initializes a new instance of the Curse class.

        Args:
            __name (str): The name of the curse.
        """
        self.__name = name

    @staticmethod
    def to_str(curse):
        """
        Convert a curse to a formatted string representation.

        Args:
            curse (dict): A dictionary representing a curse with
            'name', and 'description'.

        Returns:
            str: A formatted string representation of the curse,
            including its name and description.
        """
        item_values = []

        # Add name
        item_values.append(f"*{curse.get('name')}*.")

        # Add description
        item_values.append(f"{curse.get('description')}")

        return "\n\n".join(item_values)

    def get_list_curses(self, database):
        """
        Retrieve a list of curse names from the provided database.

        Args:
            database: A database object with a Curses collection.

        Returns:
            A list of curse names extracted from the Curses collection in the
            database.
        """
        curses = database.Curses.find({})
        return [curse.get('name') for curse in curses]

    def get_curse(self, database):
        """
        Retrieves the description and details of the curse.

        Returns:
            str: Description and details of the curse
        """
        curse = database.Curses.find_one({"name": self.__name})
        return self.to_str(curse)
