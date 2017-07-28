#!/usr/bin/env python
import re
import subprocess
import sys
import time

#get emitted list of jobs ids from 
# bsub_bldr.py using its -e option
# from stdin and wait until no longer in bjobs
#prints stderr 'Done.'

def active_job():
	#return active job ids from bjobs syscall

	proc = subprocess.Popen(["bjobs"],stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
	out,err = proc.communicate()

	jobs = list();
	for line in out.split("\n"):
		
		if not line.startswith("JOBID"):
			words = line.split(" ")
			jobid = words[0].rstrip()
			
			jobs.append(jobid)

	return jobs


if __name__ == "__main__":
	sleep_len = 1
	num_wait = 5 #num iterations to wait before update stderr

	#only print "wait" to stderr if not args provided	
	if len(sys.argv) == 1:
		do_print = True
	else:
		do_print = False


	#if any arguments provided then doesn't print "wait" to stderr
	
	#emitted job ids to wait for from stdin
	jobs = list()
	for line in sys.stdin:
		jobs.append(line.rstrip())


	#loop and sleep until no ids exist
	wait_len = 0
	num_iter = 0
	
	while True:
	
		active = active_job()
		
		if not set(jobs).isdisjoint(active):
			
			if do_print and num_iter % num_wait == 0:
				sys.stderr.write("wait. (total: "+str(wait_len)+" seconds)\n")
				num_iter = 0

			time.sleep(sleep_len)
			wait_len += sleep_len
	
			num_iter += 1
		else:
			break

	if do_print:
		sys.stderr.write("done. process completed in "+str(wait_len)+" seconds\n")
	
	exit()

