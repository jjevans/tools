#!/usr/bin/env python
import json
import bson.json_util
import sys

#convert bson
if sys.stdin.isatty():
	message = 'usage: bson_to.py (data structure on stdin)\n'
	sys.stderr.write(message)
	exit(1)

input = sys.stdin.read()
try:#try as bson
	data = bson.json_util.loads(input)
except:
	try:#as json
		data = json.loads(input)
	except:
		message = 'ERROR: unable to load json/bson:\n\t' + input + '\n'
		sys.stderr.write(message)
		exit(1)
		
print str(data)

exit()
