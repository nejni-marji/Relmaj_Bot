#!/usr/bin/env python3
import re
from random import randint
from itertools import permutations

from telegram import ParseMode
from telegram.ext import MessageHandler, Filters

from stuff.data import myself
from stuff.background import background
from stuff.constants import fullwidth

'''
This stuff is basically Nenmaj's soul. It's old and crappy, but such is the
life of Nenmaj. I can't bring myself to not include at least some of this in
Nenmaj 2.0, but I have to get rid of a lot of it. The plan is to eventually
rewrite this so that instead of calling bot_resp() a bunch of times, I'll
just have a database file somewhere that I load, and from that I'll read all
the responses I want to include.

For the time being, though, this code is gonna be garbage. Beautiful garbage.
'''

@background
def text_parse(bot, update):
	text = update.message.text
	user = update.message.from_user

	def check_at_bot():
		bot_named = re.search('(rel|nen)maj', text.lower())
		try:
			bot_replied = update.message.reply_to_message.from_user.id == bot.id
		except:
			bot_replied = False
		bot_pm = update.message.chat_id > 0
		at_bot = bot_named or bot_replied or bot_pm
		my_bot = re.search('\\b(m(y|ia) (ro)?boto?|(ro)?boto? mia)\\b', text.lower())
		master = (at_bot or my_bot) and user.id == myself
		return at_bot or master

	def bot_resp(
			pattern,
			response,
			chance = 5,
			words = True,
			markdown = False,
			call = 'text',
		):

		match = re.search(pattern, text, flags = re.I) # arg: pattern

		if words: # kwarg: words
			pattern = '\\b(%s)\\b' % pattern # arg: pattern

		match = re.search(pattern, text, flags = re.I) # arg: pattern

		bot_kwargs = {}
		bot_kwargs['reply_to_message_id'] = update.message.message_id
		bot_kwargs['parse_mode'] = ParseMode.MARKDOWN
		if not markdown:
			bot_kwargs.pop('parse_mode')

		# Bob
		if update.message.from_user.id == myself:
			bob = update.message.from_user.first_name
		else:
			bob = 'Bob'

		is_pm = update.message.chat_id > 0
		if match and chance and (randint(1, chance) == 1 or is_pm or check_at_bot()): # kwarg: chance
			response = response.format( # arg: response
				text = update.message.text,
				match = match.group(),
				match_lower = match.group().lower(),
				match_upper = match.group().upper(),
				match_capitalize = match.group().capitalize(),
				username = update.message.from_user.username,
				first_name = update.message.from_user.first_name,
				last_name = update.message.from_user.last_name,
				bob = bob,
			)

			call_list = { # kwarg: call
				'text': bot.send_message,
				'photo': bot.send_photo,
			}

			return call_list[call]( # kwarg: call
				update.message.chat_id,
				response, # arg: response
				**bot_kwargs
			)

		else:
			return False

	def bot_responses():
		# This is a goddammed massterpiece. Don't ever change, nenmaj.
		# He's changing. Welcome to the future! 2018-01-06
		# Later the same day, I just noticed the spelling of "massterpiece".
		if True:
			bot_resp(
				"^same( \w+)?$",
				"same",
			)
			bot_resp(
				"aesthetic",
				"ａｅｓｔｈｅｔｉｃ",
			)
			bot_resp(
				"#poste",
				"mdr, ĉu vere?",
				words = False,
			)
			bot_resp(
				"Skype|Skajpo?n?",
				"http://stallman.org/skype.html",
				chance = 1
			)
			bot_resp(
				"fuck me",
				"_Later?_",
				markdown = True,
			)
			bot_resp(
				"Sponge ?Bob|Square ?Pants",
				"I think the funny part was\nWith SpongeBob was just sigen\nOUT of nowhere\nAnd squeaked word was like\ncan't BELIEVE IT",
			)
			bot_resp(
				"Pizza Hut|Taco Bell",
				"http://youtu.be/EQ8ViYIeH04",
				markdown = True,
			)
			bot_resp(
				"Jesus (fucking|effing) Christ",
				"Looks more like Jesus fucking Noah to me.",
				chance = 0
			)
		if check_at_bot():
			bot_resp(
				'h(eyo?|ello|a?i|owdy)|yo|oi|greetings|sup|'
				+ 'good ((eve|mor)ning|day|afternoon)',
				'{match_capitalize}, {first_name}!',
			)
			bot_resp(
				'thanks',
				'No prob, {bob}!',
			)
			bot_resp(
				'i love (you|nenmaj)|ily|(you|nenmaj) is( the)? best (ro)?bot',
				'>///< senpai noticed me!',
			)
			bot_resp(
				'fuc?k (off|(yo)?u)|i hate (yo)?u|sod off|'
				+ 'you(\'?re? (dumb?|stupid)| suck)',
				'Please forgive me, I\'m only human!',
			)
			bot_resp(
				's+h+|be (quie|silen)t|shut up',
				'You can\'t tell me to be quiet!',
			)
		if check_at_bot():
			bot_resp(
				"(rel|nenmaj) irl|open[- ]source|source code|foss",
				"AgADAwADrKcxGxf4GEwgaG2kIA2BeI30hjEABLCGgdjm9eXSgEYBAAEC",
				call = 'photo',
			)
		if False and check_at_bot():
			for i in permutations(['mi', 'amas', 'vin']):
				bot_resp(
					' '.join(i),
					'Kaj ankaŭ {match_lower}, {first_name}!',
				)
			bot_resp(
				'saluton',
				'Resaluton, {first_name}!',
			)
			bot_resp(
				'sal',
				'Resal, {first_name}!',
			)
			bot_resp(
				'bo(vin|n((eg)?an ?)?(m(aten|oment|am)|vesper|nokt(mez)?|'
				+ '(post(?=...mez))?t(emp|ag(er|mez)?)))(eg)?on',
				'Kaj {match_lower} al vi, {first_name}!',
			)
			bot_resp(
				'dank(eg)?on',
				'Nedankinde, {first_name}!',
			)
			bot_resp(
				'hej',
				'Kion vi volas, {first_name}?',
			)
			bot_resp(
				'fek al (vi|nenmaj)|(vi|nenmaj) (estas stulta|stultas)',
				'Bonvole pardonu min, mi estas nur homo!',
			)
			bot_resp(
				'ŝ+|(kviet|silent|ferm)iĝu',
				'Vi ne povas kvietigi min!',
			)
		elif not check_at_bot():
			hello_list = ['hi', 'hello', 'hey', 'heyo']
			hello = hello_list[randint(0, len(hello_list) - 1)].capitalize()
			bot_resp(
				'h(i|ello|eyo?),? ((y\'?)?all|everyone|people|ppl)',
				hello + ', {first_name}!',
			)
		elif False and not check_at_bot():
			sal_list = ['sal', 'saluton', 'resal']
			sal = sal_list[randint(0, len(sal_list) - 1)].capitalize()
			bot_resp(
				'sal(uton)?( al|,?) (vi )?(c[hx]|ĉ)iuj?( vi)?',
				sal + ', {first_name}!',
			)

	def bot_ayylmao():
		# Don't do anything if @theayybot is present.
		try:
			theayybot = bot.get_chat_member(update.message.chat_id,
				139464619
			)
			if theayybot.status == 'member':
				return None
		except:
			pass

		res_ayy = re.search('\\b(ayy+)\\b', text.lower())
		res_lmao = re.search('\\b(lmao+)\\b', text.lower())

		if res_ayy and res_lmao:
			resp = 'ayy lmao'
		elif res_ayy:
			resp = 'lmao' + 'o' * len(res_ayy.group()[3:])
		elif res_lmao:
			resp = 'ayy' + 'y' * len(res_lmao.group()[4:])
		if res_ayy or res_lmao:
			bot.send_message(update.message.chat_id,
				resp,
			)

	my_dudes = 'It(\'?s| is) ((.+ )*(((?!, my dude).)+)),? my dudes?[.!]*$'

	def bot_my_dudes():
		try:
			text = re.search(
				my_dudes,
				update.message.text,
				flags = re.I
			).groups()[1]

			resp = ''
			for i in list(text.upper()):
				if i == ' ':
					resp += '    '
				elif i not in fullwidth:
					resp += i
				else:
					resp += chr(0xFEE0 + ord(i))

			bot.send_message(update.message.chat_id,
				resp,
				reply_to_message_id = update.message.message_id
			)

		except:
			pass

	if True:
		bot_responses()
		bot_ayylmao()
		bot_my_dudes()

def main(dp, group):
	for i in [
		MessageHandler(Filters.text, text_parse),
	]: dp.add_handler(i, group)
