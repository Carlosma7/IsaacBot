"""
This file provides a class for handling cards and runes in the game.

Author: Carlos Morales Aguilera
Date: 20-Jun-2023
"""

from difflib import SequenceMatcher
import requests
from bs4 import BeautifulSoup
from function import remove_dlc


class CardRune:
    """
    Represents a card or a rune in the game.

    Attributes:
        __name (str): The name of the card or rune.
    """

    def __init__(self, name: str):
        """
        Initializes a new instance of the CardRune class.

        Args:
            name (str): The name of the card or rune.
        """
        self.__name = name

    @staticmethod
    def get_list_cards_runes():
        """
        Retrieves a list of all the cards and runes from the game's wiki.

        Returns:
            list: A list of strings representing the names of cards and runes.
        """
        url = "https://bindingofisaacrebirth.fandom.com/wiki/Cards_and_Runes"
        result = requests.get(url, timeout=50)
        content = BeautifulSoup(result.text, 'lxml')

        cards_and_runes_tr_tag = content.find_all(
            'tr', attrs={'class': 'row-pickup'})
        cards_and_runes = []
        for card_rune in cards_and_runes_tr_tag:
            name_tag = card_rune.find('td')
            cards_and_runes.append(name_tag.get_text())
        return cards_and_runes

    def check_card_rune(self, exact):
        """
        Checks if the provided card or rune name matches any available card or rune.

        Args:
            exact (bool): Flag indicating whether an exact match is required.

        Returns:
            bool or list: If an exact match is found, returns the card or rune name (str).
                         If exact match is not required and partial matches are found,
                         returns a list of matching card or rune names.
                         Otherwise, returns False if no matches are found.
        """
        cr_name = self.__name
        cards_and_runes = [
            remove_dlc(cr.replace('\n', ''))
            for cr in CardRune.get_list_cards_runes()
        ]
        if cr_name in cards_and_runes:
            return cr_name
        if exact:
            return False
        matches = [(SequenceMatcher(None, cr, cr_name).ratio(), cr)
                   for cr in cards_and_runes]
        matches_fine = list(filter(lambda match: match[0] > 0.5, matches))
        matches_fine.sort(key=lambda tup: tup[0], reverse=True)
        matches_contained = [
            cr for cr in cards_and_runes if cr_name.lower() in cr.lower()
        ]
        if len(matches_fine) > 0 or len(matches_contained) > 0:
            matches = [match[1] for match in matches_fine] + matches_contained
            if matches_contained and matches_contained[0].lower(
            ) == cr_name.lower():
                return matches_contained[0]
            return list(dict.fromkeys(matches))

        return False

    def get_description(self, exact):
        """
        Retrieves the description and details of the card or rune.

        Args:
            exact (bool): Flag indicating whether an exact match is required.

        Returns:
            tuple: A tuple containing the card or rune information (dict) and
                   a flag indicating whether the retrieval was successful (bool).
                   The card or rune information dictionary has the following keys:
                   - 'name': The name of the card or rune (str).
                   - 'image': The URL of the card or rune image (str).
                   - 'unlock': The unlock information (str), present only for some cards/runes.
                   - 'message': The message displayed when using the card or rune (str).
                   - 'description': The description of the card or rune (str).
        """
        cards_and_runes = self.check_card_rune(exact)
        if cards_and_runes:
            if isinstance(cards_and_runes, list):
                return cards_and_runes, False
        else:
            return [], False

        url = "https://bindingofisaacrebirth.fandom.com/wiki/Cards_and_Runes"
        result = requests.get(url, timeout=50)
        content = BeautifulSoup(result.text, 'lxml')

        cards_and_runes_td_tags = content.find('td',
                                                 attrs={
                                                     'data-sort-value':
                                                     cards_and_runes
                                                 }).parent.find_all('td')

        card_rune_dict = {}
        card_rune_dict['name'] = cards_and_runes_td_tags[0].get_text()
        card_rune_dict['image'] = cards_and_runes_td_tags[2].find('img').get(
            'data-src')

        if len(cards_and_runes_td_tags) == 6:
            card_rune_dict['unlock'] = " ".join(
                cards_and_runes_td_tags[3].get_text().split())
            card_rune_dict['message'] = cards_and_runes_td_tags[4].get_text()
            card_rune_dict['description'] = " ".join(
                cards_and_runes_td_tags[5].get_text().split())
        else:
            card_rune_dict['message'] = cards_and_runes_td_tags[3].get_text()
            card_rune_dict['description'] = " ".join(
                cards_and_runes_td_tags[4].get_text().split())

        return card_rune_dict, True
