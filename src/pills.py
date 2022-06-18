import requests
from bs4 import BeautifulSoup
from difflib import SequenceMatcher
from function import remove_dlc

# Pills class
class Pill():
	def __init__(self, name: str):
		self.__name = name

	def get_list_pills():
		url = "https://bindingofisaacrebirth.fandom.com/wiki/Pills"
		respuesta = requests.get(url)
		contenido = BeautifulSoup(respuesta.text, 'lxml')

		pills_table_tag = contenido.find('table', attrs={'class': 'wikitable'})

		pills_tr_tag = pills_table_tag.find_all('tr')

		pills = []
		for pill in pills_tr_tag:
			if pill.get('id'):
				pill_td_tags = pill.find_all('td')
				pills.append(pill_td_tags[1].get_text().replace('\xa0', ''))
		return pills

	def check_pill(self, exact):
		pill_name = self.__name
		pills = [remove_dlc(pill.replace('\n', '')) for pill in Pill.get_list_pills()]
		if pill_name in pills:
			return pill_name
		if exact:
			return False
		matches = [(SequenceMatcher(None, pill, pill_name).ratio(), pill) for pill in pills]
		matches_fine = list(filter(lambda match: match[0] > 0.5, matches))
		matches_fine.sort(key=lambda tup: tup[0], reverse=True)
		matches_contained = [pill for pill in pills if pill_name.lower() in pill.lower()]
		if len(matches_fine) > 0 or len(matches_contained) > 0:
			matches = [match[1] for match in matches_fine] + matches_contained
			if matches_contained and matches_contained[0].lower() == pill_name.lower():
				return matches_contained[0]
			return list(dict.fromkeys(matches))
		else:
			return False

	def get_description(self, exact):
		pills = self.check_pill(exact)
		if pills:
			if type(pills) == list:
				return pills, False
		else:
			return [], False
		
		url = "https://bindingofisaacrebirth.fandom.com/wiki/Pills"
		respuesta = requests.get(url)
		contenido = BeautifulSoup(respuesta.text, 'lxml')

		pill_code = "_".join(pills.split())
		pills_td_tags = contenido.find('tr', attrs={'id': pill_code}).find_all('td')

		pill_dict = {}
		pill_dict['name'] = pills
		pill_dict['effect'] = pills_td_tags[2].get_text()
		pill_dict['horse'] = pills_td_tags[2].get_text()
		pill_dict['image'] = 'https://static.wikia.nocookie.net/bindingofisaacre_gamepedia/images/7/7c/Achievement_Horse_Pill_icon.png'

		return pill_dict, True
