#!/usr/bin/env python

import intstat
import sys

try:
	isfile = sys.argv[1]
	pcut = sys.argv[2]
	outfile = sys.argv[3]
except IOError as (errno, strerror):
	print "usage: is_pval.py intstat_results pvalue_cutoff output_file"

filt_obj = intstat.Filter()

with open(isfile) as handle:
	peaks = handle.readlines()
	
peaks = filt_obj.filter_by_pvalue(peaks,pcut)
	
with open(outfile,'w') as handle:
	for peak in peaks:
		handle.write(peak)
