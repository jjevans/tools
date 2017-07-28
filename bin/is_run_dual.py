#!/usr/bin/env python

####
# run IntervalStats from Olga Troyanskaya at Princeton
####
# Jason Evans, 04182012
####
import intstat
import os
import random
import sys
import time

tmpfile1 = "tmp1_"+str(time.time())+"_"+str(random.randint(1,1000000000))+".tbl"
tmpfile2 = "tmp2_"+str(time.time())+"_"+str(random.randint(1,1000000000))+".tbl"

try:
	qry = sys.argv[1]
	ref = sys.argv[2]
	dom = sys.argv[3]
	pcut = sys.argv[4]
	outfile = sys.argv[5]
except IOError as (errno, strerror):
	print "usage: is_run_dual.py query_bed reference_bed domain_bed pvalue_cutoff output_file"
	
is_obj = intstat.Run(qry,ref,dom)
filt_obj = intstat.Filter()

# run intervalstats on both query and reference
is_obj.execute2(tmpfile1,tmpfile2)

# read in intervalstats results to memory and remove file
with open(tmpfile1) as handle:
	peaks1 = handle.readlines()
os.remove(tmpfile1)

with open(tmpfile2) as handle:
	peaks2 = handle.readlines()
os.remove(tmpfile2)

# filter results by p-value
peaks1 = filt_obj.filter_by_pvalue(peaks1,pcut)
peaks2 = filt_obj.filter_by_pvalue(peaks2,pcut)

# filter all peaks that don't exist in both sets of results
dual_exist = filt_obj.filter_by_existence(peaks1,peaks2)

# write output
with open(outfile,'w') as handle:
	for record in dual_exist:
		handle.write(record+"\n")
