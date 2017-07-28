#!/usr/bin/env python
import json
import sys

for line in sys.stdin.readlines():

	try:
		data = json.loads(line.rstrip('\n'))
		
		if data.has_key('_id'):
			print data['_id'] + '\t',
		print ','.join(data.keys())
	except:
		sys.stderr.write("cannot load line: "+line)
exit

