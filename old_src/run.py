"""
This module provides functions for generating new runs, challenges, and spins in a game.

Author: Carlos Morales Aguilera
Date: 20-Jun-2023
"""

from random import randint, choice


def new_run():
    """
    Generates a new run by randomly selecting a character and a mode.

    Returns:
        str: A formatted string representing the chosen character and mode.
    """
    characters = [
        "Isaac",
        "Magdalene",
        "Cain",
        "Judas",
        "???",
        "Eve",
        "Samson",
        "Azazel",
        "Lazarus",
        "Eden",
        "The Lost",
        "Lilith",
        "Keeper",
        "Apollyon",
        "The Forgotten",
        "Bethany",
        "Jacob and Esau",
        "Tainted Isaac",
        "Tainted Magdalene",
        "Tainted Cain",
        "Tainted Judas",
        "Tainted ???",
        "Tainted Eve",
        "Tainted Samson",
        "Tainted Azazel",
        "Tainted Lazarus",
        "Tainted Eden",
        "Tainted The Lost",
        "Tainted Lilith",
        "Tainted Keeper",
        "Tainted Apollyon",
        "Tainted The Forgotten",
        "Tainted Bethany",
        "Tainted Jacob and Esau",
    ]

    mode = ["Hard", "Greed", "Greedier"]

    return f"Character: *{choice(characters)}*\nMode: *{choice(mode)}*"


def new_challenge():
    """
    Generates a new challenge by randomly selecting a challenge from a predefined list.

    Returns:
        str: A formatted string representing the chosen challenge.
    """
    challenges = [
        "1. Pitch Black",
        "2. High Brow",
        "3. Head Trauma",
        "4. Darkness Falls",
        "5. The Tank",
        "6. Solar System",
        "7. Suicide King",
        "8. Cat Got Your Tongue",
        "9. Demo Man",
        "10. Cursed!",
        "11. Glass Canon",
        "12. When Life Gives You Lemons",
        "13. Beans!",
        "14. It's in the Cards",
        "15. Slow Roll",
        "16. Computer Savvy",
        "17. Waka Waka",
        "18. The Host",
        "19. The Family Man",
        "20. Purist",
        "21. XXXXXXXXL",
        "22. SPEED!",
        "23. Blue Bomber",
        "24. PAY TO PLAY",
        "25. Have a Heart",
        "26. I RULE!",
        "27. BRAINS!",
        "28. PRIDE DAY!",
        "29. Onan's Streak",
        "30. The Guardian",
        "31. Backasswards",
        "32. Aprils Fool",
        "33. Pokey Mans",
        "34. Ultra Hard",
        "35. Pong",
        "36. Scat Man",
        "37. Bloody Mary",
        "38. Baptism by Fire",
        "39. Isaac's Awakening",
        "40. Seeing Double",
        "41. Pica Run",
        "42. Hot Potato",
        "43. Cantripped!",
        "44. Red Redemption",
        "45. DELETE THIS",
    ]

    return f"Challenge: *{choice(challenges)}*"


def new_spin():
    """
    Generates a new spin by randomly choosing between a new run and a new challenge.

    Returns:
        str: A formatted string representing the chosen spin.
    """
    spin = randint(1, 2)

    if spin == 1:
        return new_run()

    return new_challenge()
