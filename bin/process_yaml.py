#!/usr/bin/env python
import json
import yaml
import sys

try:
	file = sys.argv[1]
except:
	print "usage: try_yaml.py yaml_file"
	exit()

with open(file) as handle:
	struct = yaml.load(handle)

#print str(struct)
#print str(struct["csweb"])

print str(struct)
#print yaml.dump(struct)

exit()

