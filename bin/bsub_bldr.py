#!/usr/bin/env python
import argparse
import re
from subprocess import PIPE, STDOUT, Popen
import sys
import time

##build lsf bsub command with options

#use options or default values to 
# add resource management parameters
#submits to lsf unless disabled (-s)
#prints command to stdout unless disabled (-p)
#command must be enclosed in quotes
#individual hosts (-m) need quotes around 
# them all each host separated by space
#	ex. -m 'cmu167 cmu168" or -m cmu167
#if content in stdin, assume it is a list 
# of files to swap with the pattern inserted 
# in the specified command. dies if stdin and no pattern 
#ex echo file1 | bsub_bldr_loop.py du -h {} == du -h file1

def bld(args):
	##build entire bsub cmd
	#input is the parseargs obj "args"
	#returns fully built command
	bsub = "bsub"

	#queue 
	if args.q is not None:
		bsub += " -q "+args.q

	#hosts
	if args.m is not None:
		bsub += " -m "+args.m


	#notification email, stdout and stderr files
	if args.o:
		bsub += " -o " + filebase + ".stdout -e " + filebase + ".stderr"
		
	if args.u:#email if no files specifed
		bsub += " -u " + args.u
	
	elif not args.o:#/dev/null if no file or email provided
		bsub += " -o /dev/null -e /dev/null"


	#memory requirements
	if args.R is not None:
		bsub += " -R 'rusage[mem="+str(args.R)+"]'"

	if args.M is not None:
		bsub += " -M " + str(args.M)

	#num processors
	if args.n is not None and args.n > 1:
		bsub += " -n "+str(args.n)+" -R 'rusage[ncpus="+str(args.n)+"] span[hosts=1]'"
	else:
		bsub += " -n 1"

	
	#dependency -w done, die if orphaned
	if args.w is not None:
		bsub += " -w '"+args.cond+"("+args.w+")'"
		
	bsub += " '"+args.command+"'"


	return bsub


if __name__ == "__main__":
	
	##default values
	default_queue = "pcpgmwgs"
	default_host = None
	default_mem = 4000
	default_limit = None
	default_numproc = 1
	default_pattern = "{}"
	default_cleanup = False
	filebase = "lsf."+str(time.time())
	pair_delim = "::"
	depend_cond = "done" #done or exit


	parser = argparse.ArgumentParser()
	parser.add_argument("command")
	parser.add_argument("-q", help="lsf queue, default '"+str(default_queue)+"'", default=default_queue)

	parser.add_argument("-m", help="lsf host (nodes/group), default "+str(default_host), default=default_host)
	parser.add_argument("-n", type=int,help="number of processors, default "+str(default_numproc), default=default_numproc)

	parser.add_argument("-R", type=int,help="memory requirement (Mb), default "+str(default_mem), default=default_mem)
	parser.add_argument("-M", type=int,help="memory limit (Mb, quits job), default "+str(default_limit), default=default_limit)

	parser.add_argument("-o", help="write stdout and stderr files (basename "+filebase+"), default creates no files.", action="store_true")
	parser.add_argument("-u", help="email address for notification")

	parser.add_argument("-w", help="dependency, jobid as arg")
	parser.add_argument("-wd", help="dependency, expect list of jobids to depend on from stdin", action="store_true")
	parser.add_argument("-wp", help="dependency, expect list of jobid::pattern pairs to depend on from stdin", action="store_true")

	parser.add_argument("-e", help="emit jobids to stdout", action="store_true")
	parser.add_argument("-ep", help="emit jobid::str_to_sub pairs to stdout", action="store_true")
	parser.add_argument("-f", help="pattern to sub filenames provided on stdin, arg is the pattern to replace filename with in command provided, default '"+str(default_pattern)+"'", default=default_pattern)
	
	parser.add_argument("-p", help="do not print command to stdout", action="store_true")
	parser.add_argument("-s", help="do not submit job to cluster", action="store_true")

	args = parser.parse_args()


	args.cond = depend_cond #dependency condition
	
	#enforce providing queue if no default
	if args.q is None:
		message = "Queue unspecified yet required."
		raise Exception(message)


	##build bsub command(s)
	#check and loop over files if anything is provided in stdin
	cmds = list()
	sub_in = list() #if to emit substituted pattern by stdin, keep track of pattern to emit later
	do_sub = True #do re sub stdin to command
	

	if sys.stdin.isatty():#no stdin, build provided command
		cmds.append(bld(args))
		do_sub = False
		
		if args.wd or args.wp or args.ep:#crash if options specified that require stdin
			message = "options wd, wp, and ep require input on stdin.  None found."
			raise Exception(message)
			
	else:#filenames or jobids by stdin

		for data in sys.stdin:
			
			if args.wd:#list of jobids
				#list of lsf jobids on stdin
				args.w = data.rstrip()
				do_sub = False

			elif args.wp:#paired jobid::pattern
			
				parts = data.split(pair_delim)

				#crash unless paired correctly
				if len(parts) < 2:
					message = "ERROR: -wp option provided but stdin aren't paired by delim "+pair_delim+"\nline: "+data
					raise Exception(message)

				args.w = parts[0]
				sub_in.append(parts[1].rstrip())

			else:
				sub_in.append(data.rstrip())

			#make bsub cmd
			cmd = bld(args)

			cmds.append(cmd)

	
	#submit and get jobids
	job_pattern = "<(\d+)>" #job id from bsub output
	job_re = re.compile(job_pattern)

	##print and submit
	for i,cmd in enumerate(cmds):

		#sub in filename/pattern from stdin
		if do_sub:
		
			sub_re = re.compile(args.f)

			sub_val = sub_in[i].rstrip()

			#crash if empty pattern to sub
			if sub_val == str():
				message = "ERROR: pattern to substitute into expression is empty, line: "+str(i)
				raise Exception(message)
				
			cmd = sub_re.sub(sub_val,cmd)

		if not args.p:#print to stderr
			sys.stderr.write(cmd+"\n")


		#get job id from lsf stdout		
		jobid = None
		if not args.s:#submit job to cluster

			#proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=True)
			#stdout,stderr = proc.communicate()
			proc = Popen([cmd],stdout=PIPE,stderr=STDOUT,shell=True)
			out, err = proc.communicate()

			job_match = job_re.search(out)
			jobid = job_match.group(1)

			sys.stderr.write(out)

		if args.e:#print job id::substit_pattern (file on stdin most likely) pairs
			print str(jobid)
			
		elif args.ep:
			print str(jobid)+pair_delim+str(sub_in[i]).rstrip()

	exit(0)
