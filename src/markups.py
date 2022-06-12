import telebot

# Markups Bot API to choose similar element
def markup_similar(similarities):
	# Keyboard
	markup = telebot.types.InlineKeyboardMarkup(row_width = 1)
	# Buttons
	for elem in similarities:
		button = telebot.types.InlineKeyboardButton(elem, callback_data=elem)
		markup.add(button)

	return markup

# Markups Bot API to choose content to display
def markup_item_trinket(elem, elem_type):
	# Keyboard
	markup = telebot.types.InlineKeyboardMarkup(row_width = 2)
	# Buttons
	bt1 = telebot.types.InlineKeyboardButton('Effects', callback_data='Effects/{}/{}'.format(elem_type, elem))
	bt2 = telebot.types.InlineKeyboardButton('Notes', callback_data='Notes/{}/{}'.format(elem_type, elem))
	bt3 = telebot.types.InlineKeyboardButton('Synergies', callback_data='Synergies/{}/{}'.format(elem_type, elem))
	bt4 = telebot.types.InlineKeyboardButton('Interactions', callback_data='Interactions/{}/{}'.format(elem_type, elem))

	markup.add(bt1, bt2, bt3, bt4)

	return markup

def markup_content(elem, elem_type):
	if elem_type in ['Item', 'Trinket']:
		return markup_item_trinket(elem, elem_type)
	else:
		return False
