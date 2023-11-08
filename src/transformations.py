"""
This file provides a class for handling transformations in the game.

Author: Carlos Morales Aguilera
Date: 05-Nov-2023
"""


class Transformation:
    """
    Represents a transformation in the game.

    Attributes:
        __name (str): The name of the transformation.
    """

    def __init__(self, name: str):
        """
        Initializes a new instance of the Transformation class.

        Args:
            __name (str): The name of the transformation.
        """
        self.__name = name

    @staticmethod
    def to_str(transformation, database):
        """
        Convert a transformation to a formatted string representation.

        Args:
            transformation (dict): A dictionary representing a transformation
            with 'name', 'description', 'condition', and 'effects' keys.
            database: A database object with a Emoji collection.

        Returns:
            str: A formatted string representation of the transformation,
            including its name, description, condition and effects.
        """
        item_values = []

        # Add name
        item_values.append(f"*{transformation.get('name')}*.")

        # Add description
        item_values.append(f"{transformation.get('description')}")

        # Add condition
        item_values.append(f"Unlock: {transformation.get('condition')}")

        # Get whole content
        content = "\n\n".join(item_values)

        # Add effects
        effects = transformation.get('effects')
        if effects:
            content = [content]
            # Add effects header
            content.append("\nEffects:")

            # Get all effects
            for key, value in effects.items():
                # Retrieve emoji if defined
                emoji = database.Emojis.find_one({'key': key})
                if emoji:
                    emoji = emoji.get('value').encode('utf-8').decode(
                        'unicode_escape')
                content.append(f"• {emoji or key}: {value}.")
            content = "\n".join(content)

        return content

    def get_list_elements(self, database):
        """
        Retrieve a list of transformation names from the provided database.

        Args:
            database: A database object with a Transformations collection.

        Returns:
            A list of transformation names extracted from the Transformations
            collection in the database.
        """
        transformations = database.Transformations.find({})
        return [
            transformation.get('name') for transformation in transformations
        ]

    def get_element(self, database):
        """
        Retrieves the description and details of the transformation.

        Returns:
            str: Description and details of the transformation
        """
        transformation = database.Transformations.find_one(
            {"name": self.__name})
        return self.to_str(transformation, database)
