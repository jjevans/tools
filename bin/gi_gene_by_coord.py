#!/usr/bin/env python
import argparse
import gi_util

#pull out the gene info from a chromo position

#test case, gene GBA
chr = "1"
start = "155211000"
end = "155211500"

#default wsdl
default_wsdl = "https://geneinsight-lmm-ws.partners.org/services/Variant?wsdl"
default_user = "lmm"
default_pass = "x377BLCi"

default_gbm_wsdl = "https://geneinsight-lmm-ws.partners.org/services/GenomeBuildMapping?wsdl"

parser = argparse.ArgumentParser()
parser.add_argument("--chr",help="Chromosome (required)")
parser.add_argument("--start",help="Start position (required)")
parser.add_argument("--end",help="End position (required)")
parser.add_argument("-w","--wsdl",help="GeneInsight Variant WSDL (optional)(default GI 5.0 prod)",default=default_gbm_wsdl)
parser.add_argument("-u","--user",help="GeneInsight username (optional)(default lmm)",default=default_user)
parser.add_argument("-p","--password",help="GeneInsight password",default=default_pass)

args = parser.parse_args()

if not args.chr or not args.start or not args.end:
	raise Exception("coordinates required.  missing chromosome, start, end")

#connect to geneinsight
gi_gbm = gi_util.GI_GenomeBuildMapping(wsurl=args.wsdl,wsuser=args.user,wspass=args.password)

info = gi_gbm.region_info(args.chr,args.start,args.end)
print str(info)

exit(0)
