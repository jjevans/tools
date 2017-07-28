#!/usr/bin/env python

import gPro
import sys

##
# Enriches using the genes associated to an inputted GO term id
####
# jje 12202011
####

#term = "GO:0007050"
#gost_loc = "http://biit.cs.ut.ee/gprofiler/"

try:
	term = sys.argv[1] # GO:0000000
	outfile = sys.argv[2]
	loc = sys.argv[3]
	
except IOError as (errno, strerror):
	print "usage: gPro_by_term.py GOterm outfile gPro_URL"

# query g:Profiler
gpro_obj = gPro.Profiler(loc)
content = gpro_obj.GO_ask(term)

# parse for term enrichment
key_content = gpro_obj.break_GOSt(content)

output = open(outfile,"w")
output.write(key_content)
output.close()
