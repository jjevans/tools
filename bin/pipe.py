#!/usr/bin/env python
from subprocess import Popen,PIPE
import sys

#run pipeline on a list (ls) of filenames
#
#using all of the arguments from inputted commands, 
# run the command on all of the files from stdin

try:
	args = " ".join(sys.argv[1:])
except:
	raise Exception("No arguments to impose on inputted files")
	
#break executes
execs = args.split("|")

	


#create cmd pipes
print sys.stdin
for file in sys.stdin.readlines().rstrip():

	pipeline = None
	for i,cmd in enumerate(execs):
		
		if not pipeline:#1st cmd
			cmd += " "+file
			pipeline = [Popen([cmd],stdout=PIPE,shell=True)]
		else:

			pipeline.append(Popen([cmd],stdin=pipeline[-1].stdout,stdout=PIPE,shell=True))


		if (i == len(execs)-1) and (len(pipeline[-1].communicate()) != 0):
			print pipeline[-1].communicate()[0]

		pipeline[-1].stdout.close()

exit(0)

