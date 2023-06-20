"""
This module provides a Pill class for interacting with information about pills in the game.

It includes methods for retrieving a list of pills, checking a specific pill, and getting
the description of a pill.

Author: Carlos Morales Aguilera
Date: 20-Jun-2023
"""

from difflib import SequenceMatcher
import requests
from bs4 import BeautifulSoup
from function import remove_dlc


class Pill:
    """
    Represents a pill in the game.

    Args:
        name (str): The name of the pill.

    Attributes:
        __name (str): The private name of the pill.

    Methods:
        get_list_pills(self):
            Retrieves a list of all available pills.
        check_pill(self, exact):
            Checks if the pill exists and returns a matching pill name or a list of
            similar pill names.
        get_description(self, exact):
            Retrieves the description of the pill, including its effect and image.
    """

    def __init__(self, name: str):
        self.__name = name

    def get_list_pills(self):
        """
        Retrieves a list of all available pills.

        Returns:
            list: A list of pill names.
        """
        url = "https://bindingofisaacrebirth.fandom.com/wiki/Pills"
        result = requests.get(url, timeout=50)
        content = BeautifulSoup(result.text, 'lxml')

        pills_table_tag = content.find('table', attrs={'class': 'wikitable'})

        pills_tr_tag = pills_table_tag.find_all('tr')

        pills = []
        for pill in pills_tr_tag:
            if pill.get('id'):
                pill_td_tags = pill.find_all('td')
                pills.append(pill_td_tags[1].get_text().replace('\xa0', ''))
        return pills

    def check_pill(self, exact):
        """
        Checks if the pill exists and returns a matching pill name or a list of
        similar pill names.

        Args:
            exact (bool): Flag indicating if an exact match is required.

        Returns:
            str or list: A matching pill name or a list of similar pill names.
            False if no match is found.
        """
        pill_name = self.__name
        pills = [
            remove_dlc(pill.replace('\n', ''))
            for pill in self.get_list_pills()
        ]
        if pill_name in pills:
            return pill_name
        if exact:
            return False
        matches = [(SequenceMatcher(None, pill, pill_name).ratio(), pill)
                   for pill in pills]
        matches_fine = list(filter(lambda match: match[0] > 0.5, matches))
        matches_fine.sort(key=lambda tup: tup[0], reverse=True)
        matches_contained = [
            pill for pill in pills if pill_name.lower() in pill.lower()
        ]
        if len(matches_fine) > 0 or len(matches_contained) > 0:
            matches = [match[1] for match in matches_fine] + matches_contained
            if matches_contained and matches_contained[0].lower(
            ) == pill_name.lower():
                return matches_contained[0]
            return list(dict.fromkeys(matches))
        return False

    def get_description(self, exact):
        """
        Retrieves the description of the pill, including its effect and image.

        Args:
            exact (bool): Flag indicating if an exact match is required.

        Returns:
            dict or tuple: A dictionary containing the pill information (name,
            effect, horse, image) and a flag indicating if the pill was found.
        """
        pills = self.check_pill(exact)
        if pills:
            if isinstance(pills, list):
                return pills, False
        else:
            return [], False

        url = "https://bindingofisaacrebirth.fandom.com/wiki/Pills"
        result = requests.get(url, timeout=50)
        content = BeautifulSoup(result.text, 'lxml')

        pill_code = "_".join(pills.split())
        pills_td_tags = content.find('tr', attrs={
            'id': pill_code
        }).find_all('td')

        pill_dict = {}
        pill_dict['name'] = pills
        pill_dict['effect'] = pills_td_tags[2].get_text()
        pill_dict['horse'] = pills_td_tags[2].get_text()
        pill_dict['image'] = (
            "https://static.wikia.nocookie.net/bindingofisaacre",
            "_gamepedia/images/7/7c/Achievement_Horse_Pill_icon.png")

        return pill_dict, True
