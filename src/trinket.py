import requests
from bs4 import BeautifulSoup
from difflib import SequenceMatcher

# Trinket class
class Trinket():
	def __init__(self, name: str):
		self.__name = name
	
	def get_dlc_tag(li_tag):
		img = li_tag.contents[0]
		if img.name == 'img':
			alt_img = img.get('alt')
			if 'Added' in alt_img or 'Removed' in alt_img:
				return alt_img

		return False

	def get_text_tag(li_tag):
		dlc_tag = Trinket.get_dlc_tag(li_tag)

		if dlc_tag:
			text = '• ({0}){1}'.format(dlc_tag, li_tag.get_text().split('\n')[0])
		else:
			text = '• {}'.format(li_tag.get_text().split('\n')[0])

		# Remove extra whitespaces
		return " ".join(text.split())

	def get_sub_ul_tags(li_tag):
		# Explore sublist
		sub_ul_tags = li_tag.find_all('ul', recursive=False)

		sublist_section = []

		for ul_tag in sub_ul_tags:
			# Get list of section
			li_tags = ul_tag.find_all('li', recursive=False)

			for li_tag in li_tags:
				# Get text tag
				text_tag = Trinket.get_text_tag(li_tag)

				# Store text tag (omit close tags)
				sublist_section.append(text_tag)

				# Explore sublists
				sub_sub_list = Trinket.get_sub_ul_tags(li_tag)

				# Store sublist if not empty
				if sub_sub_list:
					sublist_section.append(sub_sub_list)

		return "\n\n".join(sublist_section)

	def get_trinket_description(trinket, content):
		trinket_dict = {}

		# Name
		trinket_dict['name'] = trinket
		
		# DLC
		dlc_box = content.find('div', attrs={'class': 'context-box'})
		if dlc_box:
			trinket_dict['dlc'] = dlc_box.find('img').get('alt').split()[-1]

		# quote
		div_quote = content.find('div', attrs={'data-source': 'quote'})
		trinket_dict['quote'] = div_quote.find('div').get_text()

		# unlock
		unlock_tag = content.find('div', attrs={'data-source': 'unlocked by'})
		if unlock_tag:
			trinket_dict['unlock'] = " ".join(unlock_tag.find('div').get_text().split())

		# image
		trinket_dict['image'] = content.find('div', attrs={'data-source': 'image'}).find_all('img')[-1].get('data-src')

		return trinket_dict

	def get_trinket_section(trinket, content, section):
		if section == 'Description':
			return Trinket.get_trinket_description(trinket, content)
		else:
			try:
				# Get section h2 tag
				h2_tag = content.find('span', attrs={'id': section})

				# Get section ul tag
				ul_tag = h2_tag.parent.next_sibling.next_sibling

				# Get list of section
				li_tags = ul_tag.find_all('li', recursive=False)

				list_section = []

				# For every element in section list, get text
				for li_tag in li_tags:
					# Get text tag
					text_tag = Trinket.get_text_tag(li_tag)

					# Store text tag (omit close tags)
					list_section.append(text_tag)

					# Explore sublists
					sub_ul_tag = Trinket.get_sub_ul_tags(li_tag)

					# Store sublist if not empty
					if sub_ul_tag:
						list_section.append(sub_ul_tag)

				section_content = "\n\n".join(list_section)

				return "*{}*\n\n{}".format(section, section_content.replace('*','x'))
			except Exception as e:
				return "No information was found for section *{}*.".format(section)

	def get_list_trinkets():
		url = "https://bindingofisaacrebirth.fandom.com/wiki/Trinkets"
		respuesta = requests.get(url)
		contenido = BeautifulSoup(respuesta.text, 'lxml')

		trinkets_tr_tag = contenido.find_all('tr', attrs={'class': 'row-trinket'})
		trinkets = []
		for trinket in trinkets_tr_tag:
			link_tag = trinket.find('a')
			trinkets.append(link_tag.get_text())
		return trinkets

	def check_trinket(self, exact):
		if exact:
			trinket_name = self.__name
		else:
			trinket_name = self.__name.title()
		
		trinkets = Trinket.get_list_trinkets()
		if trinket_name in trinkets:
			return trinket_name
		if exact:
			return False
		matches = [(SequenceMatcher(None, trinket, trinket_name).ratio(), trinket) for trinket in trinkets]
		matches_fine = list(filter(lambda match: match[0] > 0.5, matches))
		matches_fine.sort(key=lambda tup: tup[0], reverse=True)
		matches_contained = [tr for tr in trinkets if trinket_name.lower() in tr.lower()]
		if len(matches_fine) > 0 or len(matches_contained) > 0:
			matches = [match[1] for match in matches_fine] + matches_contained
			if matches_contained and matches_contained[0].lower() == trinket_name.lower():
				return matches_contained[0]
			return list(dict.fromkeys(matches))
		else:
			return False

	def get_section(self, section, exact):
		trinkets = self.check_trinket(exact)
		if trinkets:
			if type(trinkets) == list:
				return trinkets, False
		else:
			return [], False
		
		trinket_code = "_".join(trinkets.split())
		url = "https://bindingofisaacrebirth.fandom.com/wiki/{0}".format(trinket_code)

		respuesta = requests.get(url)

		contenido = BeautifulSoup(respuesta.text,'lxml')

		return Trinket.get_trinket_section(trinkets, contenido, section), True
