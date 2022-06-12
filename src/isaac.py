import requests
from bs4 import BeautifulSoup
from difflib import SequenceMatcher

def get_dlc_tag(li_tag):
	img = li_tag.contents[0]
	if img.name == 'img':
		alt_img = img.get('alt')
		if 'Added' in alt_img or 'Removed' in alt_img:
			return alt_img

	return False

def get_text_tag(li_tag):
	dlc_tag = get_dlc_tag(li_tag)

	if dlc_tag:
		text = '({0}){1}'.format(dlc_tag, li_tag.get_text().split('\n')[0])
	else:
		text = li_tag.get_text().split('\n')[0]

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
			text_tag = get_text_tag(li_tag)

			# Store text tag (omit close tags)
			sublist_section.append(text_tag)

			# Explore sublists
			sub_sub_list = get_sub_ul_tags(li_tag)

			# Store sublist if not empty
			if sub_sub_list:
				sublist_section.append(sub_sub_list)

	return "\n".join(sublist_section)

def get_item_description(item, content):
	item_dict = {}
	# DLC
	dlc_box = content.find('div', attrs={'class': 'context-box'})
	if dlc_box:
		item_dict['dlc'] = dlc_box.find('img').get('alt')

	# tipo -> active passive
	if content.find(attrs={'title': 'Items'}):
		item_dict['type'] = 'active'
	else:
		item_dict['type'] = 'passive'

	# quality
	item_dict['quality'] = content.find('div', attrs={'data-source': 'quality'}).parent.find('b').get_text()

	# quote
	div_quote = content.find('div', attrs={'data-source': 'quote'})
	item_dict['quote'] = div_quote.find('div').get_text()

	# grid
	item_dict['grid'] = content.find_all('div', attrs={'data-source': 'alias'})[1].find('i').get_text()

	# unlock
	unlock_tag = content.find('div', attrs={'data-source': 'unlocked by'})
	if unlock_tag:
		item_dict['unlock'] = " ".join(unlock_tag.find('div').get_text().split())

	return item_dict



def get_item_section(item, content, section):
	if section == 'Description':
		return get_item_description(item, content)
	else:
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
			text_tag = get_text_tag(li_tag)

			# Store text tag (omit close tags)
			list_section.append(text_tag)

			# Explore sublists
			sub_ul_tag = get_sub_ul_tags(li_tag)

			# Store sublist if not empty
			if sub_ul_tag:
				list_section.append(sub_ul_tag)

		return "\n".join(list_section)

def get_list_items():
	url = "https://bindingofisaacrebirth.fandom.com/wiki/Items"
	respuesta = requests.get(url)
	contenido = BeautifulSoup(respuesta.text, 'lxml')

	items_tr_tag = contenido.find_all('tr', attrs={'class': 'row-collectible'})
	items = []
	for item in items_tr_tag:
		link_tag = item.find('a')
		items.append(link_tag.get_text())
	return items

def check_item(item_name):
	items = get_list_items()
	if item_name in items:
		return item_name
	matches = [(SequenceMatcher(None, item, item_name).ratio(), item) for item in items]
	matches_fine = list(filter(lambda match: match[0] > 0.5, matches))
	matches_fine.sort(key=lambda tup: tup[0], reverse=True)
	if len(matches_fine) > 0:
		if len(matches_fine) > 1:
			return [match[1] for match in matches_fine]
		else:
			return matches_fine[0][1]
	else:
		return False


def get_item(item_name, section):
	items = check_item(item_name.title())
	if items:
		if type(items) == list:
			return items
	else:
		return 'No item has been found.'
	
	item_code = "_".join(items.split())
	url = "https://bindingofisaacrebirth.fandom.com/wiki/{0}".format(item_code)

	respuesta = requests.get(url)

	contenido = BeautifulSoup(respuesta.text,'lxml')

	return get_item_section(items, contenido, section)

if __name__ == "__main__":
	print(get_item("A Pony", 'Effects'))
	print()
	print('--------------')
	print()
	print(get_item("A Pony", 'Notes'))
	print()
	print('--------------')
	print()
	print(get_item("A Pony", 'Synergies'))
	print()
	print('--------------')
	print()
	print(get_item("A Pony", 'Interactions'))
	print()
	print('--------------')
	print()
	print(get_item("Black hole", 'Description'))
	print()
	print('--------------')
	print()
	print(get_item("Dead eye", 'Description'))
