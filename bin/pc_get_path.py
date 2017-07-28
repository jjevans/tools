#!/usr/bin/env python

''' get pathway details from Pathway Commons cpath ids '''

import pathcom
import sys

loc = "http://www.pathwaycommons.org/pc/webservice.do"
spec = "9606"
'''
mm 10090
arabidopsis 3702
ce 6239
rat rn 10116
Danio rerio 7955 zebrafish
dmelan 7227

'''

try:
	idfile = sys.argv[1]
	outfile = sys.argv[2]
except:
	print "usage: pc_get_path.py ids_file output_file"
	exit(1)
	
# fix ids, ids separated by comma, input to this script will be "\n"
with open(idfile) as handle:
	ids = handle.read().replace("\n",",").rstrip(",")

# query pathway commons
pc_obj = pathcom.Pathways(loc,spec)
content = pc_obj.path_details(ids)

# write answer
with open(outfile,'w') as handle:
	handle.write(content)
