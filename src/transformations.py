"""
This module provides a Transformation class that represents transformations in the game
"The Binding of Isaac: Rebirth."
It allows retrieving information about different transformations, including their effects,
requirements, and associated items.

Author: Carlos Morales Aguilera
Date: 20-Jun-2023
"""

from difflib import SequenceMatcher
import requests
from bs4 import BeautifulSoup


# Transformations class
class Transformation():
    """
    The Transformation class represents a transformation in the game
    "The Binding of Isaac: Rebirth."
    It provides methods to check and retrieve information about a specific
    transformation.
    """

    def __init__(self, name: str):
        """
        Initializes a Transformation object with the specified name.

        Parameters:
        - name (str): The name of the transformation.
        """

        self.__name = name
        self.__effects = {
            "Guppy":
            ("Grants flight and spawns a Blue Fly Removed in Repentance ",
             "each time (Added in Repentance 50% of the time) a tear hits an enemy."
             ),
            "Beelzebub":
            "Grants flight and converts small enemy flies into Blue Flies.",
            "Fun Guy":
            "+1 Red Heart Container.",
            "Seraphim":
            "Grants flight and gives +3 soul hearts.",
            "Bob":
            ("Isaac leaves a trail of green poisonous creep as he walks ",
             "that deals 6 damage per second."),
            "Spun":
            "Gives +2 damage and +0.15 speed, and spawns a random pill upon transformation.",
            "Yes Mother?":
            ("Isaac gains a stationary knife that trails directly behind him. It synergizes ",
             "like Mom's Knife Mom's Knife would."),
            "Conjoined":
            ("When attacking, the tumor faces shoot tears diagonally outwards, similar to ",
             "the effect of Added in AfterbirthThe Wiz The Wiz. Also reduces Damage by ",
             "0.3 and slightly decreases Tears."),
            "Leviathan":
            "Grants flight and gives +2 Black Heart Black Hearts.",
            "Oh Crap":
            "Whenever a pile of poop is destroyed, health is replenished by half a heart.",
            "Bookworm":
            r"Roughly 25\% of the time, Isaac shoots an extra tear, like 20/20 20/20.",
            "Adult":
            "Grants a heart container.",
            "Spider Baby":
            ("Spawns a spider familiar that applies random status effects to enemies it ",
             "comes in contact with."),
            "Stompy":
            "Taking damage has a chance to spawn rock waves.",
            "Super Bum":
            ("Replaces Bum Friend Bum Friend, Dark Bum Dark Bum, and Key Bum Key Bum for ",
             "Super Bum. This bum collects any of the other beggars' pickups, and ",
             "offers twice the rewards.")
        }
        self.__requirements = {
            "Guppy": "Picking up 3 Guppy items.",
            "Beelzebub": "Picking up 3 fly items.",
            "Fun Guy": "Picking up 3 mushroom items.",
            "Seraphim": "Picking up 3 holy items.",
            "Bob": "Picking up 3 Bob items.",
            "Spun": "Picking up 3 syringe items.",
            "Yes Mother?": "Picking up 3 Mom items.",
            "Conjoined": "Picking up 3 familiar items.",
            "Leviathan": "Picking up 3 evil items.",
            "Oh Crap": "Picking up 3 poop items.",
            "Bookworm": "Picking up 3 book items.",
            "Adult": "Picking up 3.",
            "Spider Baby": "Picking up 3 spider items.",
            "Stompy":
            "Picking up 3 items or pills that increase Isaac's size.",
            "Super Bum": "Picking up Bum Friend, Dark Bum, and Key Bum."
        }
        self.__items = {
            "Guppy": [
                "Guppy's Head", "Guppy's Paw", "Dead Cat", "Guppy's Collar",
                "Guppy's Hair Ball", "Guppy's Tail", "Guppy's Eye",
                "Kid's Drawing"
            ],
            "Beelzebub": [
                "Jar of Flies", "Plum Flute", "???'s Only Friend", "BBF",
                "Best Bud", "Big Fan", "Distant Admiration", "Forever Alone",
                "Halo of Flies", "Hive Mind", "Skatole", "Smart Fly",
                "The Mulligan", "Friend Zone", "Lost Fly", "Obsessed Fan",
                "Papa Fly", "Angry Fly", "Bot Fly", "Fruity Plum",
                "Parasitoid", "Psy Fly", "The Swarm", "YO LISTEN!"
            ],
            "Fun Guy": [
                "Mega Mush", "Wavy Cap", "1up!", "Blue Cap", "Magic Mushroom",
                "Mini Mush", "Odd Mushroom (Large)", "Odd Mushroom (Thin)",
                "God's Flesh", "Mucormycosis"
            ],
            "Seraphim": [
                "The Bible", "Dead Dove", "Holy Grail", "Holy Mantle", "Mitre",
                "Rosary", "The Halo", "Guardian Angel", "Sworn Protector",
                "Celtic Cross", "Divine Intervention", "Godhead", "Holy Light",
                "Immaculate Heart", "Revelation", "Sacred Heart", "Sacred Orb",
                "Salvation", "Scapular"
            ],
            "Bob":
            ["Bob's Rotten Head", "Bob's Brain", "Bob's Curse", "Ipecac"],
            "Spun": [
                "Experimental Treatment", "Growth Hormones", "Roid Rage",
                "Speed Ball", "Synthoil", "The Virus", "Adrenaline",
                "Euthanasia"
            ],
            "Yes Mother?": [
                "Mom's Bottle of Pills", "Mom's Bra", "Mom's Pad",
                "Mom's Shovel", "Mom's Box", "Mom's Bracelet",
                "Mom's Coin Purse", "Mom's Contacts", "Mom's Eye",
                "Mom's Eyeshadow", "Mom's Heels", "Mom's Key", "Mom's Knife",
                "Mom's Lipstick", "Mom's Perfume", "Mom's Purse",
                "Mom's Underwear", "Mom's Wig", "Mom's Pearls", "Mom's Razor",
                "Mom's Ring"
            ],
            "Conjoined": [
                "Brother Bobby", "Harlequin Baby", "Headless Baby",
                "Little Steven", "Mongo Baby", "Rotten Baby", "Sister Maggy",
                "Abel", "Acid Baby", "Boiled Baby", "Buddy in a Box",
                "Cube Baby", "Demon Baby", "Dry Baby", "Farting Baby",
                "Freezer Baby", "Ghost Baby", "Guardian Angel", "Incubus",
                "King Baby", "Lil Abaddon", "Lil Brimstone", "Lil Loki",
                "Multidimensional Baby", "Quints", "Rainbow Baby", "Robo-Baby",
                "Robo-Baby 2.0", "Seraphim", "Sworn Protector", "Twisted Pair"
            ],
            "Leviathan": [
                "The Nail", "Sulfur", "Abaddon", "Brimstone", "Pentagram",
                "Spirit of the Night", "The Mark", "The Pact",
                "Eye of the Occult", "Lord of the Pit", "Maw of the Void"
            ],
            "Oh Crap": [
                "Flush!", "The Poop", "Brown Nugget", "E. Coli", "Butt Bombs",
                "Dirty Mind", "Hallowed Ground", "Montezuma's Revenge",
                "Number Two", "Skatole"
            ],
            "Bookworm": [
                "Anarchist Cookbook", "Book of Revelations", "Book of Secrets",
                "Book of Shadows", "How to Jump", "Monster Manual",
                "Satanic Bible", "Telepathy for Dummies", "The Bible",
                "The Book of Belial", "The Book of Sin", "The Necronomicon",
                "Book of the Dead", "Lemegeton", "Book of Virtues"
            ],
            "Adult": ["Puberty"],
            "Spider Baby": [
                "Box of Spiders", "Spider Butt", "Mutant Spider",
                "Spider Bite", "Spiderbaby", "Spider Mod", "Bursting Sack",
                "Daddy Longlegs", "Hive Mind", "Infestation 2", "Juicy Sack",
                "Keeper's Kin", "Parasitoid", "Sissy Longlegs", "Sticky Bombs",
                "The Intruder"
            ],
            "Stompy": ["Leo", "Magic Mushroom"],
            "Super Bum": ["Bum Friend", "Dark Bum", "Key Bum"]
        }

    def get_list_transformations(self):
        """
        Returns a list of all available transformations in the game.

        Returns:
        - list: A list of transformation names.
        """

        return [
            'Guppy', 'Beelzebub', 'Fun Guy', 'Seraphim', 'Bob', 'Spun',
            'Yes Mother?', 'Conjoined', 'Leviathan', 'Oh Crap', 'Bookworm',
            'Adult', 'Spider Baby', 'Stompy', 'Super Bum'
        ]

    def check_transformation(self, exact):
        """
        Checks if the specified transformation exists in the game.

        Parameters:
        - exact (bool): Determines whether an exact match is required.

        Returns:
        - str or list or bool: If an exact match is found, returns the name of the transformation.
                               If not, returns a list of possible matches if any.
        """

        transformation_name = self.__name
        transformations = self.get_list_transformations()
        if transformation_name in transformations:
            return transformation_name
        if exact:
            return False
        matches = [(SequenceMatcher(None, tr, transformation_name).ratio(), tr)
                   for tr in transformations]
        matches_fine = list(filter(lambda match: match[0] > 0.5, matches))
        matches_fine.sort(key=lambda tup: tup[0], reverse=True)
        matches_contained = [
            tr for tr in transformations
            if transformation_name.lower() in tr.lower()
        ]
        if len(matches_fine) > 0 or len(matches_contained) > 0:
            matches = [match[1] for match in matches_fine] + matches_contained
            if matches_contained and matches_contained[0].lower(
            ) == transformation_name.lower():
                return matches_contained[0]
            return list(dict.fromkeys(matches))
        return False

    def get_description(self, exact):
        """
        Retrieves the description and information of the specified transformation.

        Parameters:
        - exact (bool): Determines whether an exact match is required.

        Returns:
        - tuple: A tuple containing the transformation dictionary and a boolean
        indicating if the transformation was found.
                 The transformation dictionary contains the following keys:
                 - 'name': The name of the transformation.
                 - 'effect': The effect of the transformation.
                 - 'requirements': The requirements to achieve the transformation.
                 - 'items': The list of items associated with the transformation.
                 - 'image': The URL of the transformation image.
        """

        transformations = self.check_transformation(exact)
        if transformations:
            if isinstance(transformations, list):
                return transformations, False
        else:
            return [], False

        transformation_code = "_".join(transformations.split())
        url = f"https://bindingofisaacrebirth.fandom.com/wiki/{transformation_code}"
        result = requests.get(url, timeout=50)
        content = BeautifulSoup(result.text, 'lxml')

        transformation_dict = {}
        transformation_dict['name'] = transformations
        transformation_dict['effect'] = self.__effects[transformations]
        transformation_dict['requirements'] = self.__requirements[
            transformations]
        transformation_dict['items'] = self.__items[transformations]
        if transformations != 'Stompy':
            transformation_img = content.find(
                'img', attrs={'alt': 'Isaac appearance'})
            transformation_dict['image'] = transformation_img.get('data-src')
        else:
            transformation_dict['image'] = (
                "https://static.wikia.nocookie.net/bindingofisaacre",
                "_gamepedia/images/9/98/Collectible_Leo_appearance.png")

        return transformation_dict, True
