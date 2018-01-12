#!/usr/bin/env python3
from os import execl
from os.path import dirname
from datetime import datetime

with open(dirname(__file__) + '/stuff/start.txt', 'w') as f:
	f.write(datetime.now().strftime('%s.%f'))
print('[    0.000000] running')
execl(dirname(__file__) + '/bot.py', '--')
