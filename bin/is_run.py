#!/usr/bin/env python

####
# run IntervalStats from Olga Troyanskaya at Princeton
####
# Jason Evans, 04182012
####
import intstat
import sys

pcut = 0.05

try:
	qry = sys.argv[1]
	ref = sys.argv[2]
	dom = sys.argv[3]
	outfile = sys.argv[4]
except IOError as (errno, strerror):
	print "usage: is_run_dual.py query_bed reference_bed domain_bed output_file"
	
is_obj = intstat.Run(qry,ref,dom)

# run intervalstats
is_obj.execute(outfile)

