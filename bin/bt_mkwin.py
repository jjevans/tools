#!/usr/bin/env python
import argparse
import bt
import os
import sys

#run bedtools makewindows on a bedfile
# requires input bedfile and optionally 
# a window size and step size 
#(stepsize=winsize-amount_overlap)
default_win = 2500
default_olap = 0
default_form = 'srcwinnum'
default_infh = sys.stdin
default_outfh = sys.stdout
default_gbuild = 'hg19'
default_stream = False

##arguments
parser = argparse.ArgumentParser()
parser.add_argument('-b', help='input bedfile, (optional, default stdin)', default=None)
parser.add_argument('-o', help='output bedfile (optional, default stdout)', default=None)
parser.add_argument('-i', help='bt result format (optional, default '+default_form+')', default=default_form)
parser.add_argument('-w', help='window size (optional, default 2500)', default=default_win)
parser.add_argument('-s', help='step size - amount left coord should move to right (optional, default win_size-amount_olap)', default=None)
parser.add_argument('-ol', help='amount of overlap in adjacent windows (optional, default '+str(default_olap)+')', default=default_olap)
#parser.add_argument('-g', help='reference/genome build (optional, either -b or -g, not both, only if no bed file provided, default: '+default_gbuild+')', default=default_gbuild)
parser.add_argument('-stream', help='stream results (no buffering, default: '+str(default_stream)+')', default=default_stream)

arg = parser.parse_args()


#die unless stdin or file
if arg.b is None:
	if sys.stdin.isatty():#no stdin or file so die
		parser.print_help()

		message = 'ERROR: No input.  input should be by stdin or inputted file.  niether provided.\n'
		sys.stderr.write(message)

		exit(1)

	else:
		arg.b = sys.stdin


#make step size from amount overlap if provided
if arg.s is None:
	arg.s = int(arg.w) - int(arg.ol)


##do work
bt_args = {'b':arg.b,'w':arg.w,'s':arg.s,'i':arg.i, 'stream':arg.stream}

bt_obj = bt.Mkwin(**bt_args)
wins = bt_obj.windows()

#output
if arg.o is None:
	print wins
	'''for win in wins:
		print win.each'''
else:
	wins.saveas(arg.o)


'''#out_fh.write()
if arg.o is None:
	handle = sys.stdout
else:
	try:
		handle = open(arg.o, 'w')
	except:
		message = "cannot open provided file: "+str(arg.o)
		
for win in wins:
	handle.write(

'''


exit()
