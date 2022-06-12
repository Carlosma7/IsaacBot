# Template functions for messages from Isaacbot
# Website for emojis: https://emojiterra.com/

def get_item_description(item):
	# Format all values to capitalize
	item_values = []

	# Name
	item_values.append("*{}*".format(item.get('name').upper()))
	# Quote
	item_values.append("{}".format(item.get('quote')))
	# DLC
	dlc = item.get('dlc')
	if dlc:
		if item.get('dlc') not in ['Afterbirth', 'Repentance']:
			dlc = 'Afterbirth {}'.format(dlc)
		item_values.append("Added in *{}*".format(dlc))
	# Type
	item_values.append("{} item.".format(item.get('type').capitalize()))
	if item.get('recharge'):
		item_values.append("*Recharge time*\n{}".format("\U0001f50b"*item.get('recharge')))
	# Quality
	item_values.append("*Quality*\n\u26AB\u26AB\u26AB\u26AB".replace("\u26AB", "\u2B50", item.get('quality')))
	# Grid
	item_values.append("*Grid position*\n{}".format(item.get('grid').title()))
	# Unlock Method
	if item.get('unlock'):
		item_values.append("*Unlock Method*\n{}".format(item.get('unlock').capitalize()))

	return "\n\n".join(item_values)

def get_trinket_description(trinket):
	# Format all values to capitalize
	trinket_values = []

	# Name
	trinket_values.append("*{}*".format(trinket.get('name').upper()))
	# Quote
	trinket_values.append("{}".format(trinket.get('quote')))
	# DLC
	dlc = trinket.get('dlc')
	if dlc:
		if trinket.get('dlc') not in ['Afterbirth', 'Repentance']:
			dlc = 'Afterbirth {}'.format(dlc)
		trinket_values.append("Added in *{}*".format(dlc))
	# Unlock Method
	if trinket.get('unlock'):
		trinket_values.append("*Unlock Method*\n{}".format(trinket.get('unlock').capitalize()))

	return "\n\n".join(trinket_values)

def get_card_rune_description(cr):
	card_rune_values = []

	# Name
	card_rune_values.append("*{}*".format(cr.get('name').upper()))
	# Message
	card_rune_values.append("{}".format(cr.get('message')))
	# DLC?
	# Unlock Method
	if cr.get('unlock'):
		card_rune_values.append("*Unlock Method*\n{}".format(cr.get('unlock').capitalize()))
	# Description
	card_rune_values.append("{}".format(cr.get('description')))

	return "\n\n".join(card_rune_values)

def get_element_description(elem, elem_type):
	# Item type
	if elem_type == 'Item':
		return get_item_description(elem)
	elif elem_type == 'Trinket':
		return get_trinket_description(elem)
	elif elem_type == 'CardRune':
		return get_card_rune_description(elem)
