"""
This file provides a class for handling achievements in the game.

Author: Carlos Morales Aguilera
Date: 03-Nov-2023
"""


class Achievement:
    """
    Represents an achievement in the game.

    Attributes:
        __number (int): Number ID of the achievement.
    """

    def __init__(self, number: str):
        """
        Initializes a new instance of the Achievement class.

        Args:
            number (str): Number ID of the achievement.
        """
        self.__number = number

    @staticmethod
    def to_str(achievement):
        """
        Convert an achievement to a formatted string representation.

        Args:
            achievement (dict): A dictionary representing an achievement with
            'number', 'name', 'description', and 'unlock' keys.

        Returns:
            str: A formatted string representation of the achievement,
            including its number, name, description, and unlock method.
        """
        item_values = []

        # Add name
        item_values.append(
            f"*{achievement.get('number')}. {achievement.get('name')}*.")

        # Add description
        item_values.append(f"_{achievement.get('description')}_")

        # Add unlock method
        item_values.append(f"{achievement.get('unlock')}.")

        achievement.get('name')

        return "\n\n".join(item_values)

    def check_achievement(self):
        """
        Checks if the provided achievement number matches any existing
        achievement.

        Args:
            exact (bool): Flag indicating whether an exact match is required.

        Returns:
            bool: Indicates if the achievement number is valid.
        """
        number = int(self.__number)
        return 1 <= number <= 637

    def get_element(self, database):
        """
        Retrieves the description and details of the achievement if it exists.

        Returns:
            str or bool: Whether the achievement exists or not.
        """
        if self.check_achievement():
            achievement = database.Achievements.find_one(
                {"number": self.__number})
            return self.to_str(achievement)
        return False
