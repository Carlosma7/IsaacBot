"""
This file provides a class for handling characters in the game.

Author: Carlos Morales Aguilera
Date: 08-Nov-2023
"""

# Disable similar code check which is triggered compared to
# dict formatting from Challenges entity class.
# pylint: disable=R0801


class Character:
    """
    Represents a character in the game.

    Attributes:
        __name (str): The name of the character.
    """

    def __init__(self, name: str):
        """
        Initializes a new instance of the Character class.

        Args:
            __name (str): The name of the character.
        """
        self.__name = name

    @staticmethod
    def to_str(character, database):
        """
        Convert a character to a formatted string representation.

        Args:
            character (dict): A dictionary representing a character with
            'name', 'health', 'unlock', 'pickups', 'items'
            and 'conditions' keys.

        Returns:
            str: A formatted string representation of the character,
            including its name, health, unlock method,
            pickups, items and conditions.
        """
        item_values = []

        # Add name
        item_values.append(f"*{character.get('name')}*.")

        # Add health
        item_values.append(
            Character.get_health_values('Health', character.get('health'),
                                        database))

        # Add unlock
        item_values.append(f"*Unlock method*: {character.get('unlock')}")

        # Add pickups
        if character.get('pickups'):
            item_values.append(
                Character.get_dict_values('Pickups', character.get('pickups'),
                                          database))

    # Add items
        if character.get('items'):
            item_values.append(
                Character.get_list_values('Items', character.get('items')))

        # Add conditions
        if character.get('conditions'):
            item_values.append(
                Character.get_list_values('Conditions',
                                          character.get('conditions')))

        return "\n\n".join(item_values)

    @staticmethod
    def get_health_values(section, dictionary, database):
        """
        Generate healthformatted content from a dictionary with emoji
        support.

        Args:
            section (str): The section label to include in the content.
            dictionary (dict): The dictionary containing key-value pairs to
            format.
            database: The database object for emoji retrieval.

        Returns:
            str: Formatted content with keys and values, including emoji if
            available.
        """
        content = [f"*{section}*:"]
        for key, value in dictionary.items():
            if isinstance(value, dict):
                content.append(
                    Character.get_health_values(key, value, database))
            else:
                # Retrieve emoji if defined
                emoji = database.Emojis.find_one({'key': key.title()})
                if emoji:
                    emoji = emoji.get('value').encode('utf-8').decode(
                        'unicode_escape')
                if isinstance(value, bool):
                    health = 1
                else:
                    health = int(value)
                if emoji:
                    content.append(f"• {emoji * health}")
                else:
                    content.append(f"• {key.title()}")

        return "\n".join(content)

    @staticmethod
    def get_list_values(section, list_val):
        """
        Generate formatted content from a dictionary with optional emoji
        support.

        Args:
            section (str): The section label to include in the content.
            list_val (list): The list containing key-value pairs to
            format.

        Returns:
            str: Formatted content with values.
        """
        content = [f"*{section}*:"]
        for element in list_val:
            content.append(f"• {element}")
        return "\n".join(content)

    @staticmethod
    def get_dict_values(section, dictionary, database):
        """
        Generate formatted content from a dictionary with optional emoji
        support.

        Args:
            section (str): The section label to include in the content.
            dictionary (dict): The dictionary containing key-value pairs to
            format.
            database: The database object for emoji retrieval.

        Returns:
            str: Formatted content with keys and values, including emoji if
            available.
        """
        content = [f"*{section}*:"]
        for key, value in dictionary.items():
            # Retrieve emoji if defined
            format_key = database.Emojis.find_one({'key': key.title()})
            format_val = database.Emojis.find_one({'key': str(value).title()})
            if format_key:
                format_key = format_key.get('value').encode('utf-8').decode(
                    'unicode_escape')
            if format_val:
                format_val = format_val.get('value').encode('utf-8').decode(
                    'unicode_escape')
            if isinstance(value, dict):
                content_dict = ['']
                for key_dict, value_dict in value.items():
                    format_val_dict = "\n" + "\n".join([
                        f"\t\t\t\t\t\t\t\t• {list_val}"
                        for list_val in value_dict
                    ])
                    content_dict.append(
                        f"\t\t\t\t• {key_dict.title()}: "
                        f"{format_val_dict or value_dict.title()}")

                format_val = "\n".join(content_dict)

            if isinstance(value, list):
                format_val = "\n" + "\n".join(
                    [f"\t\t\t\t• {list_val}" for list_val in value])
            content.append(f"• {format_key or key.title()}: "
                           f"{format_val or value.title()}")
        return "\n".join(content)

    def get_list_characters(self, database):
        """
        Retrieve a list of character names from the provided database.

        Args:
            database: A database object with a Characters collection.

        Returns:
            A list of character names extracted from the Characters collection
            in the database.
        """
        characters = database.Characters.find({})
        return [character.get('name') for character in characters]

    def get_character(self, database):
        """
        Retrieves the description and details of the character.

        Returns:
            str: Description and details of the character
        """
        character = database.Characters.find_one({"name": self.__name})
        return self.to_str(character, database)
