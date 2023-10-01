#!/usr/bin/env python
import argparse
import sys
from random import random

#downsample a fastq by fraction
# option to downsample by fraction
#input is a single or paired fastq, option either
#note random generator always rounds down to the sequence prior
#jje 04022018
default_ds_frac = 0.5#25% of sequence from fastq
default_fext = ".ds.fastq"

#arguments
parser = argparse.ArgumentParser()
parser.add_argument("-frac", type=float, help="downsample to this fraction of sequence (default: " + str(default_ds_frac) +")", default=default_ds_frac)
parser.add_argument("-r1", help="required, fastq file to downsample.  use with option 'r2' if paired fastqs")
parser.add_argument("-r2", help="optional, paired fastq file to r1.  unspecified indicates single end read from r1", default=None)
#parser.add_argument("-o", help="write output fastqs to file basename of this (optional, default input fastq's name, file extention: " + default_fext + ")", default=None)
args = parser.parse_args()

if args.frac < 0 or args.frac > 1:
    message = "ERROR: fraction argument must be between 0 and 1."
    sys.stderr.write(message+"\n")
    parser.print_help()
    exit()

if not args.r1:
    message = "\n#Downsample single or paired end fastqs by fraction.\n#Ouputs fastqs with input name and extension .ds.fastq.\n#Required option -r1 must be provided with a fastq file to downsample\n\n"
    sys.stderr.write(message+"\n")
    parser.print_help()
    exit()

#get number of sequences
with open(args.r1) as fh:
    num = len(list(fh.readlines()))

if num == 0:
    raise Exception("ERROR: There are zero sequences in the input file")
if num % 4 != 0:
    raise Exception("ERROR: The number of lines in the input file is not divisible by four and is not a valid fastq file")

numseq = num/4

#randomly chose sequence numbers
chosen = list()
for i in range(numseq):
    if random() <= args.frac:
        chosen.append(i*4)

topick = sorted(chosen)

#pull and write sequence
r1out = args.r1 + "." + str(args.frac) + default_fext
fh_r1 = open(r1out, 'w')

if args.r2:
    r2out = args.r2 + "." + str(args.frac) +default_fext
    fh_r2 = open(r2out, 'w')

with open(args.r1) as r1fh:
    r1 = r1fh.readlines()

if args.r2:
    with open(args.r2) as r2fh:
        r2 = r2fh.readlines()

for i in range(0, len(topick)):
    seq_r1 = r1[topick[i]:topick[i]+4]
    fh_r1.write("".join(seq_r1))

    if args.r2:
        seq_r2 = r2[topick[i]:topick[i]+4]
        fh_r2.write("".join(seq_r2))

fh_r1.close()
if args.r2:
    fh_r2.close()

print "downsampled " + str(args.frac) + " of " + str(numseq) + " sequences.\nwrote " + str(len(topick)) + " sequences to ds.fastq files.\nfile: " + r1out
if args.r2:
    print "file: " + r2out
print "done."
exit()
