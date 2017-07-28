#!/usr/bin/env python

''' get common genes within the same pathways '''

import pathcom
import sys

default_type = 'GENE_SYMBOL'

loc = "http://www.pathwaycommons.org/pc/webservice.do"
spec = "9606"
# can it run without a organism specified
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

	try:
		type = sys.argv[3]
	except:
		type = type_default
except:
	print "usage: pc_common_gene.py ids_file output_file ids_type(default "+default_type+")"
	exit(1)
	
# fix ids, ids separated by comma, input should be "\n"
with open(idfile) as handle:
	ids = handle.read().replace("\n",",").rstrip(",")

# query pathway commons
pc_obj = pathcom.Genes(loc,spec)
common = pc_obj.common_path(ids,type)

# write answer
with open(outfile,'w') as handle:
	for desc in common:
		source = common[desc].pop(0)
		
		# if at least two genes from gene list in a common pathway
		if len(common[desc]) > 1:
			genes = "\t".join(common[desc])
		
			handle.write(desc+"\t"+source+"\t"+genes+"\n")
