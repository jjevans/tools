#!/usr/bin/env python
import gi_util
import sys

# get the transcript id from genomic coordinates.
# input is a chromosome, start position, end position

# test values
#chrom=13
#start=20763342
#end=20763342

wsurl="https://geneinsight-lmm-ws.partners.org/services/GenomeBuildMapping?wsdl"
wsuser="lmm"
wspass="x377BLCi"

try:
	chrom = sys.argv[1]
	start = sys.argv[2]
	end = sys.argv[3]
except:
	print "usage: gi_tid_by_region.py chromosome start_position end_position\ntest region: chrom=13, start=20763342, end=20763342"
	exit(0)

gi_obj = gi_util.GI_GenomeBuildMapping(wsurl=wsurl,wsuser=wsuser,wspass=wspass)
tid = gi_obj.transcript_id(chrom,start,end)

if tid is None:
	print "No transcript id found."
else:
	print tid

exit(0)
