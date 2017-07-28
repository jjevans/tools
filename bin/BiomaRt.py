#!/usr/bin/env python
import biomaRt_R
import sys

####
# Query biomart utility
####
# Jason Evans, 05082012
####

mart = "ensembl"
ds = "hsapiens_gene_ensembl"

try:
	infile = sys.argv[1]
	outfile = sys.argv[2]
	att_from = sys.argv[3]
	att_to = sys.argv[4]
except:
	print "usage: BiomaRt.py ids_file output_file id_type convert_to_this_type"
	exit(0)

with open(infile) as handle:
	ids = handle.readlines()

mart_obj = biomaRt_R.Query(mart,ds)
ans = mart_obj.ask(att_to,att_from,ids)

with open(outfile,'w') as handle:
	for newid in ans[0]:
		handle.write(str(newid)+"\n")

