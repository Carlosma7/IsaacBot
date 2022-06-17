import requests
from bs4 import BeautifulSoup
from difflib import SequenceMatcher

# Item class
class Item():
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
		dlc_tag = Item.get_dlc_tag(li_tag)

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
				text_tag = Item.get_text_tag(li_tag)

				# Store text tag (omit close tags)
				sublist_section.append(text_tag)

				# Explore sublists
				sub_sub_list = Item.get_sub_ul_tags(li_tag)

				# Store sublist if not empty
				if sub_sub_list:
					sublist_section.append(sub_sub_list)

		return "\n\n".join(sublist_section)

	def get_item_description(item, content):
		item_dict = {}

		# Name
		item_dict['name'] = item
		
		# DLC
		dlc_box = content.find('div', attrs={'class': 'context-box'})
		if dlc_box:
			item_dict['dlc'] = dlc_box.find('img').get('alt').split()[-1]

		# tipo -> active passive
		if content.find(attrs={'title': 'Items'}):
			item_dict['type'] = 'active'
		else:
			item_dict['type'] = 'passive'

		# Recharge time
		recharge_tag = content.find('div', attrs={'data-source': 'recharge'})
		if recharge_tag:
			recharge_text = recharge_tag.find_all('img')[-1].parent.get_text()
			try:
				item_dict['recharge'] = int(list(filter(str.isdigit, recharge_text))[0])
			except:
				item_dict['recharge'] = recharge_text

		# quality
		item_dict['quality'] = int(content.find('div', attrs={'data-source': 'quality'}).parent.find('b').get_text())

		# quote
		div_quote = content.find('div', attrs={'data-source': 'quote'})
		item_dict['quote'] = div_quote.find('div').get_text()

		# grid
		item_dict['grid'] = content.find_all('div', attrs={'data-source': 'alias'})[1].find('i').get_text()

		# unlock
		unlock_tag = content.find('div', attrs={'data-source': 'unlocked by'})
		if unlock_tag:
			item_dict['unlock'] = " ".join(unlock_tag.find('div').get_text().split())

		# image
		item_dict['image'] = content.find('div', attrs={'data-source': 'image'}).find_all('img')[-1].get('data-src')

		return item_dict

	def get_item_section(item, content, section):
		if section == 'Description':
			return Item.get_item_description(item, content)
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
					text_tag = Item.get_text_tag(li_tag)

					# Store text tag (omit close tags)
					list_section.append(text_tag)

					# Explore sublists
					sub_ul_tag = Item.get_sub_ul_tags(li_tag)

					# Store sublist if not empty
					if sub_ul_tag:
						list_section.append(sub_ul_tag)

				section_content = "\n\n".join(list_section)

				return "*{}*\n\n{}".format(section, section_content.replace('*','x'))
			except Exception as e:
				return False

	def get_list_items():
		url = "https://bindingofisaacrebirth.fandom.com/wiki/Items"
		respuesta = requests.get(url)
		contenido = BeautifulSoup(respuesta.text, 'lxml')

		items_tr_tag = contenido.find_all('tr', attrs={'class': 'row-collectible'})
		items = []
		for item in items_tr_tag:
			link_tag = item.find('a')
			items.append(link_tag.get_text())
		# Exception: Tonsil
		items.remove('Tonsil')
		return items

	def check_item(self, exact):
		if exact:
			item_name = self.__name
		else:
			item_name = self.__name.title()

		items = Item.get_list_items()
		if item_name in items:
			return item_name
		if exact:
			return False
		matches = [(SequenceMatcher(None, item, item_name).ratio(), item) for item in items]
		matches_fine = list(filter(lambda match: match[0] > 0.5, matches))
		matches_fine.sort(key=lambda tup: tup[0], reverse=True)
		matches_contained = [it for it in items if item_name.lower() in it.lower()]
		if len(matches_fine) > 0 or len(matches_contained) > 0:
			matches = [match[1] for match in matches_fine] + matches_contained
			if matches_contained and matches_contained[0].lower() == item_name.lower():
				return matches_contained[0]
			return list(dict.fromkeys(matches))
		else:
			return False

	def get_section(self, section, exact):
		items = self.check_item(exact)
		if items:
			if type(items) == list:
				return items, False
		else:
			return [], False
		
		item_code = "_".join(items.split())
		url = "https://bindingofisaacrebirth.fandom.com/wiki/{0}".format(item_code)

		respuesta = requests.get(url)

		contenido = BeautifulSoup(respuesta.text,'lxml')

		return Item.get_item_section(items, contenido, section), True
