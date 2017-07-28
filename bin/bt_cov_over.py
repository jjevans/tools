#!/usr/bin/env python
import argparse
import bt
import sys

#tally coverage between thresholds using bedtools coverage output
# jje16, msl34
# partners personalized medicine, biofx
default_thresh = '15,30,45,60,90,120,150,200,300,400,500,1000'
default_stream = False

#input is a bamfile (required) and 
# a bedfile (required)
#thresholds a comma delim str
#optionally an output file (default stdout)

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
bt_args = {'result':arg.b, 'threshold':arg.t, "stream":arg.stream}

bt_obj = bt.Coverage(**bt_args)
cov = bt_obj.over()


#output
if arg.o is None:
	print cov
else:
	cov.saveas(arg.o)

exit()
