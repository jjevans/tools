#!/usr/bin/env python

import samtool_util
import sys

try:
	samfile = sys.argv[1]
	cleanfile = sys.argv[2]
	path = sys.argv[3]
except IOError as (errno,strerror):
	print "usage: picard_clean.py samfile cleanfile path_to_picard"
	
st_obj = samtool_util.Use()
st_obj.clean_sam(samfile,cleanfile,path)

