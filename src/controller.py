"""
This module provides a controller class for searching and retrieving information about different
game elements, including items, trinkets, cards/runes, pills, and transformations.

Author: Carlos Morales Aguilera
Date: 20-Jun-2023
"""

# pylint: disable=R0801
from item import Item
from trinket import Trinket
from cards_runes import CardRune
from pills import Pill
from transformations import Transformation


class Controller:
    """
    The Controller class handles the searching and retrieval of game element information.

    Methods:
        - search_element(query, exact=False): Searches for the given query among different game
        elements and returns the corresponding information if found.
        - get_element_section(query, exact): Retrieves a specific section of information for a
        given game element.
        - get_curses(): Retrieves information about the different curses in the game.
    """

    def search_element(self, query, exact=False):
        """
        Searches for the given query among different game elements and returns the corresponding
        information if found.

        Args:
            query (str): The query to search for.
            exact (bool): Flag indicating whether an exact match is required. (default: False)

        Returns:
            tuple: A tuple containing the result information (dict) and the type of game element
            (str) if found. If no match is found, it returns a tuple containing all the search
            results and the type 'Similar'.
        """

        # Check if query is an item
        item = Item(query)
        result_item, state = item.get_section('Description', exact)
        if state:
            return result_item, 'Item'

        # Check if query is a trinket
        trinket = Trinket(query)
        result_trinket, state = trinket.get_section('Description', exact)
        if state:
            return result_trinket, 'Trinket'

        # Check if query is a card or a rune
        card_rune = CardRune(query)
        result_card_rune, state = card_rune.get_description(exact)
        if state:
            return result_card_rune, 'CardRune'

        # Check if query is a pill
        pill = Pill(query)
        result_pill, state = pill.get_description(exact)
        if state:
            return result_pill, 'Pill'

        # Check if query is a transformation
        transformation = Transformation(query)
        result_transformation, state = transformation.get_description(exact)
        if state:
            return result_transformation, 'Transformation'

        return result_item + result_trinket + result_card_rune + \
        result_pill + result_transformation, 'Similar'

    def get_element_section(self, query, exact):
        """
        Retrieves a specific section of information for a given game element.

        Args:
            query (str): The query in the format 'section_elementType_element'.
            exact (bool): Flag indicating whether an exact match is required.

        Returns:
            str: The requested section of information for the specified game element.
        """

        section, elem_type, elem = query.split('_')

        # Get section from item
        if elem_type == 'Item':
            item = Item(elem)
            result_item, _ = item.get_section(section, exact)
            if section == 'Effects' and not result_item:
                result_item, _ = item.get_section('Effect', exact)
            if not result_item:
                return f"No information was found for section *{section}*."
            return result_item

        # Get section from trinket
        if elem_type == 'Trinket':
            trinket = Trinket(elem)
            result_trinket, _ = trinket.get_section(section, exact)
            if section == 'Effects' and not result_trinket:
                result_item, _ = item.get_section('Effect', exact)
            if not result_trinket:
                return f"No information was found for section *{section}*."
            return result_trinket
        return False

    def get_curses(self):
        """
        Retrieves information about the different curses in the game.

        Returns:
            str: Information about the different curses in a formatted string.
        """

        curses_dict = {
            "Curse of the Blind":
            ("All items are replaced with a question mark and are not revealed until they ",
             "are picked up."),
            "Curse of Darkness":
            ("The floor is much, much darker, and is only barely lit by the players natural ",
             "aura. Occasionally rooms will be filled with swirling clouds of what could be ",
             "fireflies or glowing motes of dust. Fire, explosions, and lasers will all cast ",
             "light as normal, as will red creep. (Added in Repentance) The aura of light ",
             "around Isaac is now much larger, but the darkness outside it is much darker."
             ),
            "Curse of the Lost":
            ("Removes the map from the HUD. Same effect as the Amnesia pill. Also increases ",
             "the possible total room count of the current floor to the size of the next ",
             "floor."),
            "Curse of the Maze":
            ("Entering a new room (including teleporting) will occasionally take Isaac to ",
             "the wrong room, with a screen-shake and sound effect to indicate the jump. ",
             "For example, entering the room on the right may instead take Isaac to the ",
             "room on the left. Occasionally, discovered rooms can swap contents, without ",
             "a screen-shake or sound effect. (Added in Repentance) The wrong-room effect ",
             "can now only take Isaac to undiscovered rooms."),
            "Curse of the Unknown":
            ("Removes Isaac's health from the HUD, leaving the player unable to see how many ",
             "hearts remain of any kind. Health will still be tracked as normal, including ",
             "Soul Hearts, Black Hearts, and Eternal Hearts. When Isaac is down to half a ",
             "heart, it is still marked by urine when entering a room. (Added in Repentance) ",
             "Also removes Isaac's Holy Mantle icon from the HUD."),
            "Curse of the Labyrinth":
            ("Appears only on the first floor of a chapter. Makes the floor an XL floor, which ",
             "contains two Boss Rooms, two items, and counts as two floors. If this happens ",
             "in either Basement, Cellar, or the Burning Basement, both Treasure Room doors ",
             "will be unlocked."),
            "Curse of the Cursed":
            ("Changes normal doors into cursed doors. Found only in the Cursed! challenge or ",
             "enabling the 'CVRS ED' seed."),
            "(Added in Repentance) Curse of the Giant":
            ("Merges normal sized rooms into 2x2, 1x2, 2x1, or L-shaped rooms while narrow ",
             "rooms are not affected. This curse currently isn't achievable naturally in ",
             "the game."),
        }

        curses = "*CURSES*\n\n"

        for curse, description in curses_dict.items():
            curses += f"- *{curse}*: {description}\n\n"

        return curses
