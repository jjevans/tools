#!/usr/bin/env python
import json
import sys

#convert to json
if sys.stdin.isatty():
	message = 'usage: json_to.py (data structure on stdin)\n'
	sys.stderr.write(message)
	exit(1)

gathered = str()

for line in sys.stdin.readlines():
	gathered += line.replace('\n', ' ')

print json.dumps(gathered)

exit()
