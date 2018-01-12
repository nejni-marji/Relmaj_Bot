#!/usr/bin/env python3
from os import remove
from os.path import dirname
from time import time
import logging
import importlib
from traceback import print_exc

from telegram import ParseMode
from telegram.ext import Updater, CommandHandler

from stuff.background import background
from stuff.data import token, myself

with open(dirname(__file__) + '/stuff/start.txt') as f:
	start = float(f.read())

def log_time(text):
	print('[{:12.6f}] {}'.format(time() - start, text))
log_time('imported python libraries')

log = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format = log, level=logging.INFO)
logger = logging.getLogger(__name__)

def error(bot, update, error):
	logger.warn('Update "%s" caused error "%s"' % (update, error))

updater = Updater((token))
dp = updater.dispatcher
dp.add_error_handler(error)

log_time('beginning to import bot modules')

modules = [
	'creator',
	'info',
	'status',
	'commands',
	'inline',
	'buttons',
	'text_parse',
	#'xkcd',
	#'youtube',
]

for i in enumerate(modules):
	group = i[0] + 1
	module = i[1]
	exec('import modules.%s' % module)
	exec('modules.%s.main(dp, %s)' % (module, group))
	log_time('loaded %s.py' % module)

def reload_meta(bot, update, args):
	with open(dirname(__file__) + '/stuff/start.txt', 'w') as f:
		f.write(str(start))
	if not args or not update.message.from_user.id == myself:
		return None
	if args[0] in modules:
		group = [
			i[0] for i in enumerate(modules)
			if args[0] == i[1]
		][0]
		module = modules[group]
		reload_module(bot, update, group + 1, module)
	elif args[0] == 'all':
		for i in enumerate(modules):
			reload_module(bot, update, i[0] + 1, i[1])
		reload_message = bot.send_message(
			update.message.chat_id,
			'`Done.`',
			parse_mode = ParseMode.MARKDOWN
		)
	remove(dirname(__file__) + '/stuff/start.txt')

def reload_module(bot, update, group, module):
	reload_message = bot.send_message(
		update.message.chat_id,
		'`Reloading %s.py`' % module,
		parse_mode = ParseMode.MARKDOWN
	)

	try:
		del dp.handlers[group]
		dp.groups.remove(group)

	except KeyError:
		pass

	try:
		exec('importlib.reload(%s)' % module)
		exec('%s.main(dp, %s)' % (module, group))

		bot.edit_message_text(
			chat_id = update.message.chat_id,
			message_id = reload_message.message_id,
			text = '`Reloaded %s.py`' % module,
			parse_mode = ParseMode.MARKDOWN
		)

	except:
		print_exc()

		bot.edit_message_text(
			chat_id = update.message.chat_id,
			message_id = reload_message.message_id,
			text = '`Failed to reload %s.py`' % module,
			parse_mode = ParseMode.MARKDOWN
		)

dp.add_handler(CommandHandler('reload', reload_meta, pass_args = True))
log_time('loaded reloader')
log_time('all modules loaded')

remove(dirname(__file__) + '/stuff/start.txt')

try:
	with open(dirname(__file__) + '/stuff/reboot.txt') as f:
		updater.bot.send_message(
			f.read(),
			'Reboot successful!'
		)
	remove(dirname(__file__) + '/stuff/reboot.txt')
except:
	pass

updater.start_polling()
updater.idle()
