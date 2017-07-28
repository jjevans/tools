#!/usr/bin/env python

import seq_util
import sys

lineperseq = 4 

try:
	fastq = sys.argv[1]
	num_seq = sys.argv[2]

	# buffer length, default 100Mb
	try: buff_len = int(sys.argv[3])
	except: buff_len = 100000000
	
	# option to clobber file or leave there and skip
	try: noclobber = bool(sys.argv[4]) # if defined, translates to true
	except: noclobber = False
	
except IOError as (errno,strerror):
	print "usage: break_fastq.py fastq_file number_of_seqs_per_file buffer_length_bytes clobber_file (optional) "

seq_obj = seq_util.SplitFile(num_seq,lineperseq)
files = seq_obj.split_fastq_buffer(fastq,buff_len,noclobber)

for produce in files:
	print produce
