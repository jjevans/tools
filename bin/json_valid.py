#!/usr/bin/env python
import sys
import json

#jje 10/2019
#load json to determine if it is valid

try:
	filejson = sys.argv[1]
except:
	sys.stderr.write("usage: json_valid.py file.json\n")
	exit(1)

with open(filejson) as handle:
	json.loads(handle.read())

exit()
