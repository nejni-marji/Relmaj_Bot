#!/usr/bin/env python3
from os import execl
from os.path import dirname
from sys import argv

text = 'rebooting'
num = len(text)

resp = []
resp.append('*' * (num + 6))
resp.append('== %s ==' % text.upper())
resp.append('*' * (num + 6))

print('\n'.join(resp))

with open(dirname(__file__) + '/stuff/reboot.txt', 'w') as f:
	f.write(argv[1])

execl(dirname(__file__) + '/main.py', '--')
