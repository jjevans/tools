#!/usr/bin/env python

import align_util
import sys

try:
	samfile = sys.argv[1]
	numfile = sys.argv[2]
except IOError as (errno,strerror):
	print "usage: break_sam.py sam_file number_of_files_to_produce"

aln_obj = align_util.BreakFile(samfile)

files = aln_obj.make_files(numfile)

print str(files)