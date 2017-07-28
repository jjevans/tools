#!/usr/bin/env python
import argparse
import bt
import sys

#run bedtools coverage and bin into coverage frequency ranges
# jje16, msl34
# partners personalized medicine, biofx
default_thresh = '15,30,45,60,90,120,150,200,300,400,500,1000'
default_stream = False

#input is the output intervals (counts) from bedtools 
# coverage with -split and -d options activated
#optionally an output file (default stdout)

#count num bases >thresholds (inputted) from 
# a file/pipe of output from bedtools coverage -d -split
#bins the coverage (count) over each bp in each interval
#input is
#	bt coverage output using options -split and -d.
#	options with defauts (see optional args in usage below):
#		bins - comma delim str of bin thresholds
#		input file or piped to stdin
#		output file or pipe to stdout
#		flag to disable printing header
#		(unimplemented) include averages and stddevs
#output is a table with columns:
#	chromosome
#	interval start
#	interval stop
#	length of interval
#	subsequent columns for each bin threshold
#default values
#	bins >15,>30,>45,>60,>90,>120,>150,>200,>300,>400,>500,>1000

##arguments
parser = argparse.ArgumentParser()
parser.add_argument('-b', help='coverage bedfile (optional, default stdin)')
parser.add_argument('-o', help='file to write to (optional, default stdout)')
parser.add_argument('-t', help='string of thresholds separated by comma, default='+default_thresh, default=default_thresh)
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
		arg.b = sys.stdin
		

##do work
#bt_args = {'b':arg.b, 'd':arg.d, 'split':arg.split, 'gbuild':arg.g, 'stream':arg.stream}
bt_args = {'result':arg.b, 'threshold':arg.t, "stream":arg.stream}

bt_obj = bt.Coverage(**bt_args)
tallies = bt_obj.bin()

#output
if arg.o is None:
	print cov,
else:
	cov.saveas(arg.o)


exit()
