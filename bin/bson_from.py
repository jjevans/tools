#!/usr/bin/env python
import json
import bson.json_util
import sys

#convert to json
if sys.stdin.isatty():
	message = 'usage: bson_from.py (data structure on stdin)\n'
	sys.stderr.write(message)
	exit(1)

input = sys.stdin.read()
try:#try as bson
	data = bson.json_util.dumps(input)
except:
	try:#as json
		data = json.dumps(input)
	except:
		message = 'ERROR: unable to load json/bson:\n\t' + input + '\n'
		sys.stderr.write(message)
		exit(1)
		
print str(data)

exit()
