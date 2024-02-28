"""
This file provides a class for handling items in the game.

Author: Carlos Morales Aguilera
Date: 21-Nov-2023
"""

from difflib import SequenceMatcher


class Item:
    """
    Represents a item in the game.

    Attributes:
        __name (str): The name of the item.
    """

    def __init__(self, name: str):
        """
        Initializes a new instance of the Item class.

        Args:
            __name (str): The name of the item.
        """
        self.__name = name

    @staticmethod
    def to_str(item):
        """
        Convert a item to a formatted string representation.

        Args:
            item (dict): A dictionary representing a item
            with 'name', 'unlock', 'description', 'message', 'effect',
            'notes', 'interactions' and 'synergies' keys.
            database: A database object with a Emoji collection.

        Returns:
            str: A formatted string representation of the item,
            including its name, unlock method, description, message, effects,
            notes, interactions and synergies.
        """
        item_values = []

        print(item)

        # Add name
        item_values.append(f"*{item.get('name')}*.")

        # Add message
        item_values.append(f"_{item.get('message')}_.")

        # Add description
        item_values.append(f"{item.get('description')}.")

        # Add description
        item_values.append(f"*Unlock method*: {item.get('unlock')}.")

        # Add quality
        item_values.append(f"*Quality*: {item.get('quality')}.")

        # Add recharge
        item_values.append(f"*Recharge*: {item.get('recharge')}.")

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
        item_content = [f"*{section}*:"]
        for element in list_val:
            item_content.append(f"• {element}")
        return "\n".join(item_content)

    def get_list_elements(self, database, query, exact):
        """
        Retrieve a list of item names from the provided database.

        Args:
            database: A database object with a Items collection.
            query: Item name to find.
            exact: Whether to retrieve a item or a list of possible results.

        Returns:
            A list of item names extracted from the Items
            collection in the database.
        """
        items = database.Items.find({})
        items = [item.get('name') for item in items]
        result_items = []

        if query in items:
            return query
        if exact:
            return False

        for item in items:
            similarity_ratio = SequenceMatcher(None, query, item).ratio()
            if similarity_ratio > 0.5:
                result_items.append(item)
        if len(result_items) == 0:
            return []
        return result_items

    def get_element(self, database):
        """
        Retrieves the description and details of the item.

        Returns:
            str: Description and details of the item
        """
        item = database.Items.find_one({"name": self.__name})
        return self.to_str(item)

    def get_element_section(self, database, section):
        """
        Retrieves the section from the element.

        Returns:
            section (str): Section to retrieve.
        """
        item = database.Items.find_one({"name": self.__name})
        values = item.get(section.lower())
        item_content = [f"*{section}*:"]

        for value in values:
            tabs = "\t\t\t\t"
            item_format_val = value[1].lstrip()
            item_content.append(f"{tabs * int(value[0])}• {item_format_val}")

        return "\n\n".join(item_content)
