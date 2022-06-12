from random import randint, choice


def new_run():
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

    mode = ["Hard", "Creed"]

    return "Character: *{}*\nMode: *{}*".format(choice(characters), choice(mode))


def new_challenge():
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

    return "Challenge: *{}*".format(choice(challenges))


def new_spin():
    spin = randint(1, 2)

    if spin == 1:
        return new_run()

    return new_challenge()
