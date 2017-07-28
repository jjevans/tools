#!/usr/bin/env python

import seq_util
import sys

try:
	fastq = sys.argv[1]
	num_seq = sys.argv[2]
except IOError as (errno,strerror):
	print "usage: break_fastq.py fastq_file number_of_seqs_per_file"

seq_obj = seq_util.SplitFile(num_seq)
files = seq_obj.split_fastq(fastq)

for produce in files:
	print produce
