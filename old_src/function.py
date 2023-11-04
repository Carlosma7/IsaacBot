"""
This module contains a utility function for removing DLC tags from a string.

Functions:
    remove_dlc: Remove DLC tags from a string.

Author: Carlos Morales Aguilera
Date: 20-Jun-2023
"""

def remove_dlc(element):
    """
    Removes the leading space character from the given element if it exists.

    Args:
        element (str): The element to be processed.

    Returns:
        str: The modified element with the leading space character removed, if present.
    """
    return element if (element[0] != ' ') else element[1:]
