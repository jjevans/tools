#!/usr/bin/env python
import argparse
import bt
import sys

#run bedtools coverage
# jje16, msl34
# partners personalized medicine, biofx

#input is a bamfile (required) and 
# a bedfile (required)
#optionally an output file (default stdout)
# 	split (don't fill gaps, default True
# 	d (depth (cov) at each pos)
#	strand (require same strand (True), diff strand (False),
#		(default both -d and -split)
default_gbuild = 'hg19'
default_stream = False

##arguments
parser = argparse.ArgumentParser()
#parser.add_argument('abam', help='bam file to assess coverage, required', default=None)
parser.add_argument('abam')
parser.add_argument('-b', help='bed file of intervals (optional, default intervals on stdin)', default=None)
parser.add_argument('-d', help='count at each position (default True)', action='store_true')
parser.add_argument('-g', help='reference/genome build (optional, either -b or -g, not both, only if no bed file provided, default '+default_gbuild+')', default=default_gbuild)
parser.add_argument('-o', help='file to write to (optional, default stdout)')
parser.add_argument('-split', help='allow short match/mismatch/gap or only from whole instervals (default True)', action='store_true')
parser.add_argument('-stream', help='stream results (no buffering, default: '+str(default_stream)+')', default=default_stream)

arg = parser.parse_args()


#die unless stdin or file
if arg.b is None:
	if sys.stdin.isatty():#no stdin or file so die
		parser.print_help()

		message = 'ERROR: No input.  input bam should be by stdin or inputted file.  niether provided.\n'
		sys.stderr.write(message)

		exit(1)

	else:
		arg.b = sys.stdin.read()


#output
output = None
if arg.o is None:#stdout
	output = sys.stdout

else:#to file

	try:
		output = open(arg.o,'w')
	except:
		message = 'cannot open file for output: '+arg.o
		raise Exception(message)
		
	
##do work
bt_args = {'abam':arg.abam, 'b':arg.b, 'd':arg.d, 'split':arg.split, 'gbuild':arg.g, 'stream':arg.stream}

bt_obj = bt.Coverage(**bt_args)
bt_obj.run()


#write
if arg.o is None:
	for res in bt_obj.result:
		print res,
else:
	bt_obj.saveas(arg.o)

exit()
