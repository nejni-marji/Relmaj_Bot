#!/usr/bin/env python3
from telegram.ext import MessageHandler, Filters

from stuff.data import myself

def status(bot, update):
	try:
		if update.message.left_chat_member.id == bot.id:
			bot.send_message(myself,
				'{} ({}) has removed me from a chat:\n{}:\n{}'.format(
					update.message.from_user.first_name,
					update.message.from_user.id,
					update.message.chat.title,
					update.message.chat_id
				)
			)
	except AttributeError:
		pass

def main(dp, group):
	for i in [
		MessageHandler(Filters.status_update, status),
	]: dp.add_handler(i, group)
