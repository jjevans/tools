#!/usr/bin/env python

import samtool_util
import sys

try:
	bamfile = sys.argv[1]
	outprefix = sys.argv[2]
except:
	print "usage: st_sort.py bamfile output_file_prefix"
	exit(0);
	
st_obj = samtool_util.Use()
bamfile = st_obj.sort_bam(bamfile,outprefix)

print bamfile
