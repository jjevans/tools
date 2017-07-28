#!/usr/bin/env python

import lsf_util
import os
import sys

tmpfile = "lsf_out.txt"
lsfarg = "-q pcpgm -R 'rusage[mem=10000]' -o " + tmpfile
outstart = "The output"
outend = "Sender:"

try:
	samfile = sys.argv[1]
	outfile = sys.argv[2]
	num_align = sys.argv[3]
        queue = sys.argv[4]
except:
	print "usage: lsf_split_sort.py samfile bamoutput num_align_per_sort lsf_queue"
        exit()

''' break large sam file into smaller pieces of sam files '''	
cmd = 'piece.py'
cmdarg = [samfile,num_align]

tmpfile = "lsf_out.txt"
lsfarg = "-q "+queue+" -R 'rusage[mem=10000]' -o " + tmpfile
outstart = "The output"
outend = "Sender:"

lsf_obj = lsf_util.LSF(lsfarg)

jobid = lsf_obj.submit(cmd,cmdarg)

lsf_obj.wait(jobid)

''' sort each file '''
cmd = "st_sort.py"

jobs = list()
trip = False

with open(tmpfile) as handle:
	lines = handle.readlines()

# remove these files to cleanup after run
samfiles = list()
bamfiles = list()

mergefiles = list()
mergefiles.append(outfile)

for line in lines:
		
	if trip is True and line != "\n":
		samfile = line.rstrip("\n")
		jobs.append(lsf_obj.submit(cmd,[samfile]))
		
		samfiles.append(samfile)
		bamfiles.append(samfile+".bam")
		mergefiles.append(samfile+".bam")
		
	if line.startswith(outstart):
		trip = True
		
lsf_obj.sync(jobs)

''' merge sorted files '''
cmd = "st_merge.py"

jobid = lsf_obj.submit(cmd,mergefiles)
lsf_obj.wait(jobid)


''' clean up '''
lsf_obj.delete_job()

os.remove(tmpfile)
for tmp in samfiles:
	os.remove(tmp)
for tmp in bamfiles:
	os.remove(tmp)
