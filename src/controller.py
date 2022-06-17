from item import Item
from trinket import Trinket
from cards_runes import CardRune

# Controller class
class Controller():
	def search_element(self, query, exact=False):
		# Check if query is an item
		item = Item(query)
		result_item, state = item.get_section('Description', exact)
		if state:
			return result_item, 'Item'

		# Check if query is a trinket
		trinket = Trinket(query)
		result_trinket, state = trinket.get_section('Description', exact)
		if state:
			return result_trinket, 'Trinket'

		# Check if query is a card or a rune
		card_rune = CardRune(query)
		result_card_rune, state = card_rune.get_description(exact)
		if state:
			return result_card_rune, 'CardRune'
		return result_item + result_trinket + result_card_rune, 'Similar'


	def get_element_section(self, query, exact):
		section, elem_type, elem = query.split('_')

		# Get section from item
		if elem_type == 'Item':
			item = Item(elem)
			result_item, state = item.get_section(section, exact)
			if section == 'Effects' and not result_item:
				result_item, state = item.get_section('Effect', exact)
			if not result_item:
				return "No information was found for section *{}*.".format(section)
			return result_item

		# Get section from trinket
		if elem_type == 'Trinket':
			trinket = Trinket(elem)
			result_trinket, state = trinket.get_section(section, exact)
			if section == 'Effects' and not result_trinket:
				result_item, state = item.get_section('Effect', exact)
			if not result_trinket:
				return "No information was found for section *{}*.".format(section)
			return result_trinket
