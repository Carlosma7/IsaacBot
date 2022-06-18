import requests
from bs4 import BeautifulSoup
from difflib import SequenceMatcher
from function import remove_dlc

# Cards and Runes class
class CardRune():
	def __init__(self, name: str):
		self.__name = name

	def get_list_cards_runes():
		url = "https://bindingofisaacrebirth.fandom.com/wiki/Cards_and_Runes"
		respuesta = requests.get(url)
		contenido = BeautifulSoup(respuesta.text, 'lxml')

		cards_and_runes_tr_tag = contenido.find_all('tr', attrs={'class': 'row-pickup'})
		cards_and_runes = []
		for cr in cards_and_runes_tr_tag:
			name_tag = cr.find('td')
			cards_and_runes.append(name_tag.get_text())
		return cards_and_runes

	def check_card_rune(self, exact):
		cr_name = self.__name
		cards_and_runes = [remove_dlc(cr.replace('\n', '')) for cr in CardRune.get_list_cards_runes()]
		if cr_name in cards_and_runes:
			return cr_name
		if exact:
			return False
		matches = [(SequenceMatcher(None, cr, cr_name).ratio(), cr) for cr in cards_and_runes]
		matches_fine = list(filter(lambda match: match[0] > 0.5, matches))
		matches_fine.sort(key=lambda tup: tup[0], reverse=True)
		matches_contained = [cr for cr in cards_and_runes if cr_name.lower() in cr.lower()]
		if len(matches_fine) > 0 or len(matches_contained) > 0:
			matches = [match[1] for match in matches_fine] + matches_contained
			if matches_contained and matches_contained[0].lower() == cr_name.lower():
				return matches_contained[0]
			return list(dict.fromkeys(matches))
		else:
			return False

	def get_description(self, exact):
		cards_and_runes = self.check_card_rune(exact)
		if cards_and_runes:
			if type(cards_and_runes) == list:
				return cards_and_runes, False
		else:
			return [], False
		
		url = "https://bindingofisaacrebirth.fandom.com/wiki/Cards_and_Runes"
		respuesta = requests.get(url)
		contenido = BeautifulSoup(respuesta.text, 'lxml')

		cards_and_runes_td_tags = contenido.find('td', attrs={'data-sort-value': cards_and_runes}).parent.find_all('td')

		card_rune_dict = {}
		card_rune_dict['name'] = cards_and_runes_td_tags[0].get_text()
		card_rune_dict['image'] = cards_and_runes_td_tags[2].find('img').get('data-src')

		if len(cards_and_runes_td_tags) == 6:
			card_rune_dict['unlock'] = " ".join(cards_and_runes_td_tags[3].get_text().split())
			card_rune_dict['message'] = cards_and_runes_td_tags[4].get_text()
			card_rune_dict['description'] = " ".join(cards_and_runes_td_tags[5].get_text().split())
		else:
			card_rune_dict['message'] = cards_and_runes_td_tags[3].get_text()
			card_rune_dict['description'] = " ".join(cards_and_runes_td_tags[4].get_text().split())

		return card_rune_dict, True
