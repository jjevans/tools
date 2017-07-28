#!/usr/bin/env python

import seq_util
import sys

try:
	fastq = sys.argv[1]
	num_seq = sys.argv[2]
	outfile = sys.argv[3]
except IOError as (errno,strerror):
	print "usage: break_fastq.py fastq_file number_of_seqs_per_file file_for_filenames_produced"

seq_obj = seq_util.SplitFile(num_seq)
files = seq_obj.split_fastq(fastq)

with open(outfile,'w') as handle:
	for produced in files:
		handle.write(produced+"\n")

