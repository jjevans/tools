#!/usr/bin/env python
import json
import sys

#convert from json
if sys.stdin.isatty():
	message = 'usage: json_from.py (json on stdin)\n'
	sys.stderr.write(message)
	exit(1)

gathered = str()

for line in sys.stdin.readlines():
	gathered += line.replace('\n', ' ')

print json.loads(gathered)

exit()
