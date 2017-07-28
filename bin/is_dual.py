#!/usr/bin/env python

####
# run IntervalStats from Olga Troyanskaya at Princeton
####
# Jason Evans, 04182012
####
import intstat
import sys

try:
	isfile1 = sys.argv[1]
	isfile2 = sys.argv[2]
	pcut = sys.argv[3]
	outfile = sys.argv[4]
except IOError as (errno, strerror):
	print "usage: is_dual.py IntStat_file1 IntStat_file2 output_file"

filt_obj = intstat.Filter()

with open(isfile1) as handle:
	peaks1 = handle.readlines()
	
peaks1 = filt_obj.filter_by_pvalue(peaks1,pcut)

with open(isfile2) as handle:
	peaks2 = handle.readlines()

peaks2 = filt_obj.filter_by_pvalue(peaks2,pcut)

dual_exist = filt_obj.filter_by_existence(peaks1,peaks2)

with open(outfile,'w') as handle:
	for record in dual_exist:
		handle.write(record+"\n")

