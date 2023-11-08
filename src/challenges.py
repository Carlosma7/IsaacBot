"""
This file provides a class for handling challenges in the game.

Author: Carlos Morales Aguilera
Date: 05-Nov-2023
"""


class Challenge:
    """
    Represents a challenge in the game.

    Attributes:
        __name (str): The name of the challenge.
    """

    def __init__(self, name: str):
        """
        Initializes a new instance of the Challenge class.

        Args:
            __name (str): The name of the challenge.
        """
        self.__name = name

    @staticmethod
    def to_str(challenge, database):
        """
        Convert a challenge to a formatted string representation.

        Args:
            challenge (dict): A dictionary representing a challenge with
            'name', 'character', 'conditions', 'goal', 'unlock' and 'prize'
            keys.

        Returns:
            str: A formatted string representation of the challenge,
            including its name, character, conditions, goal, unlock method and
            prize.
        """
        item_values = []

        # Add name
        item_values.append(f"*{challenge.get('name')}*.")

        # Add character
        item_values.append(
            Challenge.get_dict_values(
                'Character', challenge.get('character'), database))

        # Add conditions
        item_values.append(
            Challenge.get_dict_values(
                'Conditions', challenge.get('conditions'), database))

        # Add goal
        item_values.append(f"*Goal:* {challenge.get('goal')}.")

        # Add unlock method
        if challenge.get('unlock') != 'Default':
            item_values.append(f"*Unlock method:* {challenge.get('unlock')}.")

        # Add prize
        item_values.append(f"*Prize:* {challenge.get('prize')}.")

        return "\n\n".join(item_values)

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
                format_key = "Items"
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

    def get_list_challenges(self, database):
        """
        Retrieve a list of challenge names from the provided database.

        Args:
            database: A database object with a Challenges collection.

        Returns:
            A list of challenge names extracted from the Challenges collection
            in the database.
        """
        challenges = database.Challenges.find({})
        return [challenge.get('name') for challenge in challenges]

    def get_challenge(self, database):
        """
        Retrieves the description and details of the challenge.

        Returns:
            str: Description and details of the challenge
        """
        challenge = database.Challenges.find_one({"name": self.__name})
        return self.to_str(challenge, database)
