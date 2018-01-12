#!/usr/bin/env python3
from os import execl
from os.path import dirname
from time import sleep, time
from datetime import datetime, timedelta
from psutil import cpu_percent, virtual_memory

from telegram.ext import CommandHandler, MessageHandler, Filters

from stuff.data import myself

with open(dirname(__file__) + '/../stuff/start.txt') as f:
	start = float(f.read())

def bot_reboot(bot, update):
	if not update.message.from_user.id == myself:
		return None
	msg = bot.send_message(update.message.chat_id,
		'Rebooting...',
	)
	sleep(1)
	data = str(msg.chat_id)
	execl(dirname(__file__) + '/../reboot.py', '--', data)

def bot_shutdown(bot, update):
	if not update.message.from_user.id == myself:
		return None
	bot.send_message(update.message.chat_id,
		'Shutting down...',
	)
	sleep(1)
	execl(dirname(__file__) + '/../shutdown.py', '--')

def bot_system(bot, update):
	resp = []
	# get ping
	delta = datetime.now() - update.message.date
	resp.append('Ping: ' + str(delta))
	# get uptime
	date = datetime(1, 1, 1) + timedelta(seconds = time() - start)
	now = datetime.now().strftime('%H:%M:%S')
	days = date.day-1
	hours = date.strftime('%H:%M:%S')
	if days:
		resp.append('Uptime: {}, {} days, {}'.format(now, days, hours))
	else:
		resp.append('Uptime: {}, {}'.format(now, hours))
	# get cpu
	cpu = cpu_percent()
	# get ram
	ram = virtual_memory().percent
	resp.append('CPU: %.3f%%' % cpu)
	resp.append('RAM: %.3f%%' % ram)
	# send message
	bot.send_message(update.message.chat_id,
		'\n'.join(resp),
		reply_to_message_id = update.message.message_id,
	)

def notify(bot, update):
	if update.message.from_user.id in (myself, bot.id):
		return None

	member = bot.get_chat_member(
		update.message.chat_id,
		myself
	)
	unreadable = not member.status in ('creator', 'administrator', 'member')
	private = update.message.chat_id > 0

	if unreadable or private:
		bot.forward_message(
			chat_id = myself,
			from_chat_id = update.message.chat_id,
			message_id = update.message.message_id
		)

def main(dp, group):
	for i in [
		CommandHandler('reboot', bot_reboot),
		CommandHandler('shutdown', bot_shutdown),
		CommandHandler('system', bot_system),
		MessageHandler(Filters.all, notify),
	]: dp.add_handler(i, group)
