#!/usr/bin/env python
import json
import sys

for line in sys.stdin.readlines():

	try:
		data = json.loads(line.rstrip('\n'))
		
		for arg in sys.argv[1:]:
			if data.has_key(arg):
				print data[arg] + '\t',
			else:
				print "None\t",
		print ""
	except:
		sys.stderr.write("cannot load line: "+line)
exit

