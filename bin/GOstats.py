#!/usr/bin/env python

""" Run the Bioconductor GOstats package using RPy 
	to annotate genes with Gene Ontology terms 
	
	Jason Evans
	
	Usage: run_gostats.py infile outfile ontology database p-value_cutoff
	
	Input is a list of Entrez gene ids.
"""

import GOstats_R
import sys

try:
	infile = sys.argv[1]
	outfile = sys.argv[2]
	ontology = sys.argv[3]
	db = sys.argv[4]
	pcut = sys.argv[5]
except IOError as (errno, strerror):
	print "usage: GO_Annotation.py infile outfile"

''' open and read in ids '''
with open(infile) as handle:
	content = handle.read()
ids = content.split("\n")

""" create an instance of RPy to run GOstats """
go_obj = GOstats_R.Use(ids,ontology,db,pcut)
res_obj = go_obj.run()

# remember to uncomment removed() methods and __init__ for Res()
#res_obj = go_obj.hg_res_obj_from_source()

''' get the summary and produce strings of features for each GO term '''
summary_dict = res_obj.smry_dict()

""" produce the output and write to file """
''' each line from get_param() trails with 3 spaces ("   ") '''
out_str = go_obj.get_param()+"\n"

''' removed ids trail with 3 tabs '''
out_str += "ids not found in gene universe: "+res_obj.removed()+"\t\t\t\n\n"

out_str += "GO Term\tP-value\tExpected\tObserved\tGene Count\tDescription\n"

for item in summary_dict:
	out_str += summary_dict[item]
	
with open(outfile,'w') as handle:
	handle.write(out_str)
