"""
This module provides a Trinket class for retrieving information about trinkets from the game
"The Binding of Isaac: Rebirth".
It utilizes web scraping techniques to fetch data from the game's fandom wiki page.

Author: Carlos Morales Aguilera
Date: 20-Jun-2023
"""

from difflib import SequenceMatcher
import requests
from bs4 import BeautifulSoup

# pylint: disable=broad-except


class Trinket:
    """
    A class that represents a trinket.

    Attributes:
        __name (str): The name of the trinket.

    Methods:
        __init__(self, name: str): Initializes a new instance of the Trinket class.
        get_dlc_tag(self, li_tag): Retrieves the DLC tag from a list item tag.
        get_text_tag(self, li_tag): Retrieves the text tag from a list item tag.
        get_sub_ul_tags(self, li_tag): Retrieves the sublist tags from a list item tag.
        get_trinket_description(self, trinket, content): Retrieves the description of a trinket.
        get_trinket_section(self, trinket, content, section): Retrieves a specific section of a
        trinket's information.
        get_list_trinkets(self): Retrieves a list of all trinkets.
        check_trinket(self, exact): Checks if a trinket exists.
        get_section(self, section, exact): Retrieves a specific section of information
        for a trinket.
    """

    def __init__(self, name: str):
        """
        Initializes a new instance of the Trinket class.

        Args:
            name (str): The name of the trinket.
        """
        self.__name = name

    def get_dlc_tag(self, li_tag):
        """
        Retrieves the DLC tag from a list item tag.

        Args:
            li_tag: The list item tag.

        Returns:
            The DLC tag if found, False otherwise.
        """
        img = li_tag.contents[0]
        if img.name == 'img':
            alt_img = img.get('alt')
            if 'Added' in alt_img or 'Removed' in alt_img:
                return alt_img
        return False

    def get_text_tag(self, li_tag):
        """
        Retrieves the text tag from a list item tag.

        Args:
            li_tag: The list item tag.

        Returns:
            The formatted text tag.
        """
        dlc_tag = self.get_dlc_tag(li_tag)
        text_li_tag = li_tag.get_text().split('\n')[0]
        if dlc_tag:
            text = f"• ({dlc_tag}){text_li_tag}"
        else:
            text = f"• {text_li_tag}"
        # Remove extra whitespaces
        return " ".join(text.split())

    def get_sub_ul_tags(self, li_tag):
        """
        Retrieves the sublist tags from a list item tag.

        Args:
            li_tag: The list item tag.

        Returns:
            The combined sublist sections.
        """
        sub_ul_tags = li_tag.find_all('ul', recursive=False)
        sublist_section = []
        for ul_tag in sub_ul_tags:
            li_tags = ul_tag.find_all('li', recursive=False)
            for tag in li_tags:
                text_tag = self.get_text_tag(tag)
                sublist_section.append(text_tag)
                sub_sub_list = self.get_sub_ul_tags(tag)
                if sub_sub_list:
                    sublist_section.append(sub_sub_list)
        return "\n\n".join(sublist_section)

    def get_trinket_description(self, trinket, content):
        """
        Retrieves the description of a trinket.

        Args:
            trinket: The trinket.
            content: The content of the trinket page.

        Returns:
            A dictionary containing the trinket's description, name, DLC, quote, and
            image.
        """
        trinket_dict = {}
        trinket_dict['name'] = trinket
        dlc_box = content.find('div', attrs={'class': 'context-box'})
        if dlc_box:
            trinket_dict['dlc'] = dlc_box.find('img').get('alt').split()[-1]
        div_quote = content.find('div', attrs={'data-source': 'quote'})
        trinket_dict['quote'] = div_quote.find('div').get_text()
        unlock_tag = content.find('div', attrs={'data-source': 'unlocked by'})
        if unlock_tag:
            trinket_dict['unlock'] = " ".join(
                unlock_tag.find('div').get_text().split())
        trinket_dict['image'] = content.find(
            'div', attrs={
                'data-source': 'image'
            }).find_all('img')[-1].get('data-src')
        return trinket_dict

    def get_trinket_section(self, trinket, content, section):
        """
        Retrieves a specific section of a trinket's information.

        Args:
            trinket: The trinket.
            content: The content of the trinket page.
            section: The section to retrieve.

        Returns:
            The formatted section content if found, a message otherwise.
        """
        if section == 'Description':
            return self.get_trinket_description(trinket, content)
        try:
            h2_tag = content.find('span', attrs={'id': section})
            ul_tag = h2_tag.parent.next_sibling.next_sibling
            li_tags = ul_tag.find_all('li', recursive=False)
            list_section = []
            for li_tag in li_tags:
                text_tag = self.get_text_tag(li_tag)
                list_section.append(text_tag)
                sub_ul_tag = self.get_sub_ul_tags(li_tag)
                if sub_ul_tag:
                    list_section.append(sub_ul_tag)
            section_content = "\n\n".join(list_section)
            return f"*{section}*\n\n{section_content.replace('*', 'x')}"
        except Exception:
            return f"No information was found for section *{section}*."

    def get_list_trinkets(self):
        """
        Retrieves a list of all trinkets.

        Returns:
            A list of trinket names.
        """
        url = "https://bindingofisaacrebirth.fandom.com/wiki/Trinkets"
        result = requests.get(url, timeout=50)
        content = BeautifulSoup(result.text, 'lxml')
        trinkets_tr_tag = content.find_all('tr',
                                             attrs={'class': 'row-trinket'})
        trinkets = []
        for trinket in trinkets_tr_tag:
            link_tag = trinket.find('a')
            trinkets.append(link_tag.get_text())
        return trinkets

    def check_trinket(self, exact):
        """
        Checks if a trinket exists.

        Args:
            exact: Determines if an exact match is required.

        Returns:
            The trinket name if found, a list of possible matches if not exact, False otherwise.
        """
        if exact:
            trinket_name = self.__name
        else:
            trinket_name = self.__name.title()
        trinkets = self.get_list_trinkets()
        if trinket_name in trinkets:
            return trinket_name
        if exact:
            return False
        matches = [(SequenceMatcher(None, trinket,
                                    trinket_name).ratio(), trinket)
                   for trinket in trinkets]
        matches_fine = list(filter(lambda match: match[0] > 0.5, matches))
        matches_fine.sort(key=lambda tup: tup[0], reverse=True)
        matches_contained = [
            tr for tr in trinkets if trinket_name.lower() in tr.lower()
        ]
        if len(matches_fine) > 0 or len(matches_contained) > 0:
            matches = [match[1] for match in matches_fine] + matches_contained
            if matches_contained and matches_contained[0].lower(
            ) == trinket_name.lower():
                return matches_contained[0]
            return list(dict.fromkeys(matches))
        return False

    def get_section(self, section, exact):
        """
        Retrieves a specific section of information for a trinket.

        Args:
            section: The section to retrieve.
            exact: Determines if an exact match is required.

        Returns:
            A tuple containing the section content and a boolean indicating if the trinket
            was found.
        """
        trinkets = self.check_trinket(exact)
        if trinkets:
            if isinstance(trinkets, list):
                return trinkets, False
        else:
            return [], False
        trinket_code = "_".join(trinkets.split())
        url = f"https://bindingofisaacrebirth.fandom.com/wiki/{trinket_code}"
        result = requests.get(url, timeout=50)
        content = BeautifulSoup(result.text, 'lxml')
        return self.get_trinket_section(trinkets, content, section), True
