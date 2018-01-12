#!/usr/bin/env python3
from telegram import ParseMode
from telegram.ext import CommandHandler

def info_meta(bot, update, args):
	commands = {
		'user':    info_user,
		'chat':    info_chat,
		'message': info_message,
		'forward': info_forward,
		'json' :   info_json,
	}
	try:
		commands[args[0]](bot, update, args)
	except:
		usage = [i for i in commands]
		usage.sort()
		resp = 'Usage: `/info [{}]`'.format('|'.join(usage))
		bot.send_message(update.message.chat_id,
			resp,
			parse_mode = ParseMode.MARKDOWN,
		)

def info_user(bot, update, args):
	if not update.message.reply_to_message:
		return None

	member = bot.get_chat_member(
		update.message.chat_id,
		update.message.reply_to_message.from_user.id
	)
	user = member.user

	resp = [str(user.id)]
	if user.username:
		resp[0] += ' (@%s)' % user.username
	resp += ['Forename: %s' % user.first_name]
	if user.last_name:
		resp += ['Surname: %s' % user.last_name]
	if update.message.chat_id < 0:
		resp += ['Status: %s' % member.status]

	bot.send_message(update.message.chat_id,
		'\n'.join(resp),
		reply_to_message_id = update.message.message_id
	)

def info_chat(bot, update, args):
	chat = update.message.chat
	resp = '{}:\n{}'.format(chat.title, chat.id)
	bot.send_message(update.message.chat.id,
		resp,
		reply_to_message_id = update.message.message_id
	)

def info_message(bot, update, args):
	if not update.message.reply_to_message:
		return None
	resp = update.message.reply_to_message.message_id
	bot.send_message(update.message.chat_id,
		resp,
		reply_to_message_id = update.message.message_id
	)

def info_forward(bot, update, args):
	if not update.message.reply_to_message:
		return None
	if not update.message.reply_to_message.forward_from:
		return None
	user = update.message.reply_to_message.forward_from

	resp = [str(user.id)]
	if user.username:
		resp[0] += ' (@%s)' % user.username
	resp += ['Forename: %s' % user.first_name]
	if user.last_name:
		resp += ['Surname: %s' % user.last_name]

	bot.send_message(update.message.chat_id,
		'\n'.join(resp),
		reply_to_message_id = update.message.message_id
	)

def info_json(bot, update, args):
	if not update.message.reply_to_message:
		return None
	if update.message.chat_id < 0:
		resp = 'I\'ll PM you the message data (if you don\'t receive it, you may not have started this bot).'
		bot.send_message(update.message.chat_id,
			resp,
			reply_to_message_id = update.message.message_id
		)
	bot.send_message(update.message.from_user.id,
		str(update.message.reply_to_message)
	)

def main(dp, group):
	for i in [
		CommandHandler('info', info_meta, pass_args = True),
		CommandHandler('i', info_meta, pass_args = True),
		CommandHandler('iu', info_user, pass_args = True),
		CommandHandler('ic', info_chat, pass_args = True),
		CommandHandler('im', info_message, pass_args = True),
		CommandHandler('if', info_forward, pass_args = True),
		CommandHandler('ij', info_json, pass_args = True),
	]: dp.add_handler(i, group = group)
