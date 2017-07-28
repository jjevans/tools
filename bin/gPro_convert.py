#!/usr/bin/env python

import gPro
import sys

##
# Runs gConvert from g:Profiler to convert ids
####
# jje 10152011
####

#gost_loc = "http://biit.cs.ut.ee/gprofiler/"
#ci_loc = "http://biit.cs.ut.ee/gprofiler/gconvert.cgi"

try:	
	idfile = sys.argv[1]
	outfile = sys.argv[2]
	loc = sys.argv[3]
	type = sys.argv[4] #from 1-3, hgnc=1,entrez=2,ensg=3
	
except:
	print "usage: gPro_convert.py infile outfile gPro:URL new_id_type"
	exit()

''' open and read in ids '''
with open(idfile) as ids:
	id_raw = ids.read()

# format ids from a list to space delim string
id_form = id_raw.replace("\n"," ")

ci_obj = gPro.Convert_ID(loc)

if type is "1": #hgnc
	ci_cont = ci_obj.to_hgnc(id_form)
elif type is "2": #entrez
	ci_cont = ci_obj.to_entrez(id_form)
elif type is "3": #ensg
	ci_cont = ci_obj.to_ensg(id_form)
else:
	raise ValueError("1=hgnc,2=entrez,3=ensg")

	
print ci_cont

output = open(outfile,"w")
output.write(ci_cont)	
output.close()
