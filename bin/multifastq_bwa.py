#!/usr/bin/env python

import align_util
import lsf_util
import seq_util
import subprocess
import sys

try:
	left_fastq = sys.argv[1]
	right_fastq = sys.argv[2]
	num_seq = int(sys.argv[3])
	prefix = sys.argv[4]
	
	try: lsf = sys.argv[5]
	except: lsf = None
	
except IOError as (errno,strerror):
	print "usage: multifastq_bwa.py fastq_left fastq_right number_seqs_per_file bwa_db_prefix"

seq_obj = seq_util.SplitFile(num_seq)
bwa_obj = align_util.BWA(prefix)

left_files = seq_obj.split_fastq(left_fastq)
right_files = seq_obj.split_fastq(right_fastq)

samfiles = bwa_obj.multifastq_call(left_files,right_files)

print str(samfiles)

'''

thread = 12
	
seq1_obj = seq_util.SplitFile(left_fastq,num_seq)
seq2_obj = seq_util.SplitFile(right_fastq,num_seq)

left_files = seq1_obj.split_fastq()
right_files = seq2_obj.split_fastq()

for i,x in enumerate(left_files):

	outsai1 = left_files[i]+".sai"
	outsai2 = right_files[i]+".sai"
	
	cmdaln1 = ['bwa','aln',prefix,left_files[i],'-t',str(thread),'-f',outsai1]
	cmdaln2 = ['bwa','aln',prefix,right_files[i],'-t',str(thread),'-f',outsai2]

	outsam = "paired."+str(i)+".sam"
	cmdpe = ['bwa','sampe',prefix,outsai1,outsai2,left_files[i],right_files[i],'-f',outsam]
	
	subprocess.check_call(cmdaln1)
	subprocess.check_call(cmdaln2)
	subprocess.check_call(cmdpe)
	
	print outsam
'''
