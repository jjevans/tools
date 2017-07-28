#!/usr/bin/env python
import align_util
import sys

try:
	samfile = sys.argv[1]
	num_align = sys.argv[2]
except IOError as (errno, strerror):
	print "usage: sortpiece.py samfile num_align_per_sort"
	
align_obj = align_util.SplitFile(samfile,num_align)
files = align_obj.split_file()

print "\n".join(files)
