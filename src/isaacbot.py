from controller import Controller
from template import *
from markups import *
from run import *

import telebot
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path = '.env')

TOKEN = os.getenv('TOKEN')

if not TOKEN:
	TOKEN = input('\nPlease enter a valid Telegram Bot Token: ')

bot = telebot.TeleBot(TOKEN)
controller = Controller()

@bot.message_handler(commands=['start'])
def start(message):
	bot.send_photo(message.chat.id, photo="https://www.somosxbox.com/wp-content/uploads/2021/11/The-Binding-of-Isaac-Repentance-scaled.jpg", caption="Hi! My name is Isaac! \n\nWelcome to The Binding of Isaac: Rebirth unofficial bot.", parse_mode="Markdown")

@bot.message_handler(commands=['spin'])
def spin(message):
	bot.send_message(message.chat.id, new_spin(), parse_mode="Markdown")

@bot.message_handler(commands=['run'])
def spin(message):
	bot.send_message(message.chat.id, new_run(), parse_mode="Markdown")

@bot.message_handler(commands=['challenge'])
def spin(message):
	bot.send_message(message.chat.id, new_challenge(), parse_mode="Markdown")

@bot.message_handler(commands=['curses'])
def curses(message):
	bot.send_message(message.chat.id, controller.get_curses(), parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def query(message):
	result, res_type = controller.search_element(message.text)
	if type(result) == dict:
		bot.send_photo(message.chat.id, photo=result['image'], caption=get_element_description(result, res_type), parse_mode="Markdown", reply_markup=markup_content(message.text, res_type))
	else:
		bot.send_message(message.chat.id, '"{}" was not found, but here are some similar possibilities.'.format(message.text), reply_markup=markup_similar(result))

@bot.callback_query_handler(lambda call: '_' in call.data)
def query_content(call):
	result = controller.get_element_section(call.data, True)
	
	bot.send_message(call.message.chat.id, result, parse_mode="Markdown")

@bot.callback_query_handler(lambda call: '_' not in call.data)
def query_similar(call):
	# Exception Options? item is not processable
	if call.data == 'Options?':
		bot.send_message(call.message.chat.id, 'Since we cannot process this item, here is the direct link to [Options?](https://bindingofisaacrebirth.fandom.com/wiki/Options%3F)', parse_mode="Markdown")
	else:
		result, res_type = controller.search_element(call.data, True)
		bot.delete_message(call.message.chat.id, call.message.id)
		bot.send_photo(call.message.chat.id, photo=result['image'], caption=get_element_description(result, res_type), parse_mode="Markdown", reply_markup=markup_content(call.data, res_type))

bot.polling()
