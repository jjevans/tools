#!/usr/bin/env python
import argparse
import sys
import time
import jobs
import json
from copy import deepcopy
import multiprocessing
import os

#check genotypes between all inputted vcfs for a set of bed positions
#does all combos of comparison.  input is two or more vcfs and a bedfile of marker position
batchsize = 1000
gt_boost = 99

def _parse_args():
        ap = argparse.ArgumentParser(description='Identify identical samples from a set of genotypes at a set of bed file positions')

        ap.add_argument('--out', help='The file of output', required=False, default="out.txt")
        ap.add_argument('-n', help='Number of cores to use', type=int, required=False, default=multiprocessing.cpu_count())
        ap.add_argument('-b','--bed', help='bed file of marker positions to confirm genotype', required=True)
        ap.add_argument('--vcf', action="append", help='input files to process')

        return ap.parse_args()

if __name__ == '__main__':
        args = _parse_args()

        if len(list(args.vcf)) < 2:
                message = "ERROR: comparison requires at least two vcfs (--vcf) provided as argumnents.\n"
                raise Exception(message)


	#index vcf if .vcf.gz.tbi not exist
	indexcmds = list()
	for vcf in args.vcf:
		tbi = vcf + ".tbi"
		if not os.path.exists(tbi):
			cmd = "bcftools index -f --tbi " + vcf
			indexcmds.append([cmd])

	#run indexing of vcfs if needed
	if len(indexcmds) > 0:
		jobs_obj = jobs.Process(nt=args.n)
		jobs_obj.run_pipes(indexcmds)

		for pid in jobs_obj.pids:
			if jobs_obj.pids[pid]["returncode"] is not None and jobs_obj.pids[pid]["returncode"] != 0:
				message += str(jobs_obj.pids[pid])
				raise Exception(message+"\n")


        #output file
	fh = sys.stdout
	if args.out is not None:
		fh = open(args.out,'w')

        #iterate all for compare with bcftools gtcheck
	#multithread
	jobs_obj = jobs.Process(nt=args.n, do_throw=True)

	cmds = list()
        for i, vcf1 in enumerate(args.vcf):

                for j, vcf2 in enumerate(args.vcf[i+1:]):
			#outfile = bcf1 + "---" + bcf2 + "." + args.suffix
			cmd_tup = list()
			cmd = "bcftools gtcheck -G " + str(gt_boost) + " -T " + args.bed + " -g " + vcf1 + " " + vcf2 
			cmd_tup.append(cmd)
			cmd = "bcft_gtck_tbl.pl"
			cmd_tup.append(cmd)
			cmds.append(cmd_tup)

	#run commands in batches of size batchsize
	i = 0
	while i < len(cmds):
		#run batch of jobs	
        	jobs_obj = jobs.Process(nt=args.n)
		jobs_obj.run_pipes(cmds[i:i+batchsize])
		
		
	        for pid in jobs_obj.pids:
			if jobs_obj.pids[pid]["returncode"] is not None and jobs_obj.pids[pid]["returncode"] != 0:
				message += str(jobs_obj.pids[pid])
				raise Exception(message+"\n")

			
			if jobs_obj.pids[pid]["endpoint"] is True:
				fh.write(str(jobs_obj.pids[pid]["stdout"]).rstrip()+"\n")

		i += batchsize
        exit()
