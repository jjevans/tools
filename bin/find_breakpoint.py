#!/usr/bin/env python

import align_util
import sys

try:
	samfile = sys.argv[1]
	numfile = int(sys.argv[2])
except IOError as (errno,strerror):
	print "usage: find_breakpoint.py samfile num_files_to_break_into\n"
	
aln_obj = align_util.BreakFile(samfile)
bp = aln_obj.break_points(numfile)
print bp
