"""
This file provides a class for handling trinkets in the game.

Author: Carlos Morales Aguilera
Date: 08-Nov-2023
"""

from difflib import SequenceMatcher


class Trinket:
    """
    Represents a trinket in the game.

    Attributes:
        __name (str): The name of the trinket.
    """

    def __init__(self, name: str):
        """
        Initializes a new instance of the Trinket class.

        Args:
            __name (str): The name of the trinket.
        """
        self.__name = name

    @staticmethod
    def to_str(trinket):
        """
        Convert a trinket to a formatted string representation.

        Args:
            trinket (dict): A dictionary representing a trinket
            with 'name', 'unlock', 'description', 'message', 'effect',
            'notes', 'interactions' and 'synergies' keys.
            database: A database object with a Emoji collection.

        Returns:
            str: A formatted string representation of the trinket,
            including its name, unlock method, description, message, effects,
            notes, interactions and synergies.
        """
        item_values = []

        # Add name
        item_values.append(f"*{trinket.get('name')}*.")

        # Add message
        item_values.append(f"_{trinket.get('message')}_.")

        # Add description
        item_values.append(f"{trinket.get('description')}.")

        # Add description
        item_values.append(f"*Unlock method*: {trinket.get('unlock')}.")

        return "\n\n".join(item_values)

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

    def get_list_elements(self, database, query, exact):
        """
        Retrieve a list of trinket names from the provided database.

        Args:
            database: A database object with a Trinkets collection.
            query: Trinket name to find.
            exact: Whether to retrieve a trinket or a list of possible results.

        Returns:
            A list of trinket names extracted from the Trinkets
            collection in the database.
        """
        trinkets = database.Trinkets.find({})
        trinkets = [trinket.get('name') for trinket in trinkets]
        result_trinkets = []

        if query in trinkets:
            return query
        if exact:
            return False

        for trinket in trinkets:
            similarity_ratio = SequenceMatcher(None, query, trinket).ratio()
            if similarity_ratio > 0.5:
                result_trinkets.append(trinket)
        if len(result_trinkets) == 0:
            return False
        return result_trinkets

    def get_element(self, database):
        """
        Retrieves the description and details of the trinket.

        Returns:
            str: Description and details of the trinket
        """
        trinket = database.Trinkets.find_one({"name": self.__name})
        return self.to_str(trinket)

    def get_element_section(self, database, section):
        """
        Retrieves the section from the element.

        Returns:
            section (str): Section to retrieve.
        """
        trinket = database.Trinkets.find_one({"name": self.__name})
        values = trinket.get(section.lower())
        content = [f"*{section}*:"]

        for value in values:
            tabs = "\t\t\t\t"
            format_val = value[1].lstrip()
            content.append(f"{tabs * int(value[0])}• {format_val}")

        return "\n\n".join(content)
