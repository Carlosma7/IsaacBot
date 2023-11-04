"""
This module provides template functions for generating descriptions of various
game elements in Isaacbot.

Author: Carlos Morales Aguilera
Date: 20-Jun-2023
"""

# Template functions for messages from Isaacbot
# Website for emojis: https://emojiterra.com/

def get_item_description(item):
    """
    Generates a description for an item.

    Args:
        item (dict): A dictionary containing item information.

    Returns:
        str: The formatted description of the item.
    """
    # Format all values to capitalize
    item_values = []

    # Name
    item_values.append(f"*{item.get('name').upper()}*")
    # Quote
    item_values.append(f"{item.get('quote')}")
    # DLC
    dlc = item.get('dlc')
    if dlc:
        if item.get('dlc') not in ['Afterbirth', 'Repentance']:
            dlc = f"Afterbirth {dlc}"
        item_values.append(f"Added in *{dlc}*")
    # Type
    item_values.append(f"{item.get('type').capitalize()} item.")
    if item.get('recharge'):
        if isinstance(item.get('recharge'), int):
            charges = "\U0001f50b" * item.get('recharge')
            item_values.append(f"*Recharge time*\n{charges}")
        else:
            item_values.append(f"*Recharge time*\n{item.get('recharge')[1:].capitalize()}")
    # Quality
    quality = "*Quality*\n\u26AB\u26AB\u26AB\u26AB".replace("\u26AB", "\u2B50", item.get('quality'))
    item_values.append(quality)
    # Grid
    item_values.append(f"*Grid position*\n{item.get('grid').title()}")
    # Unlock Method
    if item.get('unlock'):
        item_values.append(f"*Unlock Method*\n{item.get('unlock').capitalize()}")

    return "\n\n".join(item_values)

def get_trinket_description(trinket):
    """
    Generates a description for a trinket.

    Args:
        trinket (dict): A dictionary containing trinket information.

    Returns:
        str: The formatted description of the trinket.
    """
    # Format all values to capitalize
    trinket_values = []

    # Name
    trinket_values.append(f"*{trinket.get('name').upper()}*")
    # Quote
    trinket_values.append(f"{trinket.get('quote')}")
    # DLC
    dlc = trinket.get('dlc')
    if dlc:
        if trinket.get('dlc') not in ['Afterbirth', 'Repentance']:
            dlc = f"Afterbirth {dlc}"
        trinket_values.append(f"Added in *{dlc}*")
    # Unlock Method
    if trinket.get('unlock'):
        trinket_values.append(f"*Unlock Method*\n{trinket.get('unlock').capitalize()}")

    return "\n\n".join(trinket_values)

def get_card_rune_description(card_rune):
    """
    Generates a description for a card or rune.

    Args:
        cr (dict): A dictionary containing card or rune information.

    Returns:
        str: The formatted description of the card or rune.
    """
    card_rune_values = []

    # Name
    card_rune_values.append(f"*{card_rune.get('name').upper()}*")
    # Message
    card_rune_values.append(f"{card_rune.get('message')}")
    # DLC?
    # Unlock Method
    if card_rune.get('unlock'):
        card_rune_values.append(f"*Unlock Method*\n{card_rune.get('unlock').capitalize()}")
    # Description
    card_rune_values.append(f"{card_rune.get('description')}")

    return "\n\n".join(card_rune_values)

def get_pill_description(pill):
    """
    Generates a description for a pill.

    Args:
        pill (dict): A dictionary containing pill information.

    Returns:
        str: The formatted description of the pill.
    """
    pill_values = []

    # Name
    pill_values.append(f"*{pill.get('name').upper()}*")
    # Effect
    pill_values.append(f"*Effect*\n{pill.get('effect')}")
    # Horse effect
    pill_values.append(f"*Horse effect*\n{pill.get('horse')}")

    return "\n\n".join(pill_values)

def get_transformation_description(transformation):
    """
    Generates a description for a transformation.

    Args:
        transformation (dict): A dictionary containing transformation information.

    Returns:
        str: The formatted description of the transformation.
    """
    transformation_values = []

    # Name
    transformation_values.append(f"*{transformation.get('name').upper()}*")
    # Effect
    transformation_values.append(f"*Effects*\n{transformation.get('effect')}")
    # Requirements
    transformation_values.append(f"*Requirements*\n{transformation.get('requirements')}")
    # Items
    items = ""
    for item in transformation.get('items'):
        items += f"• {item}\n"
    transformation_values.append(f"*Possible Items*\n{items}")

    return "\n\n".join(transformation_values)

def get_element_description(elem, elem_type):
    """
    Generates a description for a game element based on its type.

    Args:
        elem (dict): A dictionary containing element information.
        elem_type (str): The type of the element (e.g., 'Item', 'Trinket',
        'CardRune', 'Pill', 'Transformation').

    Returns:
        str: The formatted description of the game element.
    """
    # Item type
    if elem_type == 'Item':
        return get_item_description(elem)
    if elem_type == 'Trinket':
        return get_trinket_description(elem)
    if elem_type == 'CardRune':
        return get_card_rune_description(elem)
    if elem_type == 'Pill':
        return get_pill_description(elem)
    if elem_type == 'Transformation':
        return get_transformation_description(elem)
    return False
