#!/usr/bin/env python

#import samtool_util
import shutil
import subprocess
import sys

try:
	outfile = sys.argv[1]
	bams = sys.argv[2:]
except IOError as (errno, strerror):
	print "usage: sortpiece.py samfile bamfiles"

''' if only one bam to merge, just copy the file to the desired output file instead of merging '''
if len(bams) == 1:
	shutil.copy(bams[0],outfile)
else:
	cmd = ["samtools","merge"]
	cmd.append(outfile)
	cmd.extend(bams)

	subprocess.check_call(cmd)



