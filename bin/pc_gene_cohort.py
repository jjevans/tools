#!/usr/bin/env python

import pathcom
import sys

loc = "http://www.pathwaycommons.org/pc/webservice.do"
spec = "9606" #human

try:
	idfile = sys.argv[1]
	idtype = sys.argv[2]
	outfile = sys.argv[3]
except:
	print "usage: pc_gene_cohort.py ids_file ids_type output_file"
	exit(1)
	
# fix ids, ids separated by comma, input should be "\n"
with open(idfile) as handle:
	ids = handle.read().replace("\n",",").rstrip(",")

# query pathway commons
####
# get pathways for genes
pc_obj = pathcom.Pathways(loc,spec)
paths = pc_obj.path_by_id(ids)

# get other genes in those pathways
gene_obj = pathcom.Genes(loc,spec)
content = gene_obj.gene_by_path(paths)

# write answer
with open(outfile,'w') as handle:
	handle.write(content)
