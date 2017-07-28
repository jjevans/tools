#!/usr/bin/env python

import gPro
import sys

##
# Runs the GOst profiler from g:Profiler
####
# jje 10152011
####

#term = "GO:0007050"
#gost_loc = "http://biit.cs.ut.ee/gprofiler/"

try:
	idfile = sys.argv[1]
	outfile = sys.argv[2]
	loc = sys.argv[3]
	spec = sys.argv[4]
	pcut = sys.argv[5]
	
except IOError as (errno, strerror):
	print "usage: gPro_profile.py infile outfile gPro_URL p-value_cutoff"

''' open and read in ids '''
with open(idfile) as ids:
	id_raw = ids.read()

# convert ids from a list to space delim string
id_form = id_raw.replace("\n"," ")

gpro_obj = gPro.Profiler(loc,spec)
content = gpro_obj.ask_pcut(id_form,pcut)

# parse for term enrichment
key_content = gpro_obj.break_GOSt(content)

output = open(outfile,"w")
output.write(key_content)	
output.close()

