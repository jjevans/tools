#!/usr/bin/env python

import os
import samtool_util
import shutil
import subprocess
import sys

''' produces bam and index named by the input samfile name with a 
	.bam and .bai extension on them '''

usage = "usage: groom_sam.py samfile output_bamfile path_to_picard output_bamindex (optional)"

try:
	samfile = sys.argv[1]
	bamout = sys.argv[2]	
	path = sys.argv[3]

	try: 
		indexout = sys.argv[4]
	except: 
		indexout = None
		print usage
		exit(0)
except:
#except IOError as (errno,strerror):
	print usage
	exit(0)

''' temporary filenames '''
cleanfile = samfile + ".clean.sam"
cleanbam = cleanfile + ".bam"

st_obj = samtool_util.Use()

st_obj.clean_sam(samfile,cleanfile,path)
print "sam file clean."

# returns samfile.bam (with .bam extension), same as temporary bamfile name
bamfile = st_obj.sort_sam(cleanfile)
shutil.move(bamfile,bamout)

print "sam file sorted and converted to bam."

if indexout is not None:
	st_obj.index(bamout,indexout)
	print "bam file indexed."

''' remove all but output bam file and output bam index '''
#os.remove(cleanfile)
#os.remove(cleanbam)

print "Done."
